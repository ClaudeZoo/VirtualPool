__author__ = 'Claude'

import re
import use_shell
import send_socket
import time
import random


def get_vm_state(uuid):
    state_tuple = use_shell.shell("vboxmanage showvminfo %s --machinereadable" % uuid)
    state_re = re.compile(r'VMState="(.*?)"')
    match = state_re.search(state_tuple[0])
    if match:
        return match.group(1)

def start_vm(reply_dict):
    uuid = reply_dict["vm_uuid"]
    vm_state = get_vm_state(uuid)
    if (vm_state != 'running') and (vm_state != 'paused'):
        command = "vboxmanage startvm %s --type headless" % uuid
        stdout_stderr_tuple = use_shell.shell(command)
        if stdout_stderr_tuple[1] != None:
            reply_dict["request_result"] = "execution_error"
            reply_dict["error_information"] = stdout_stderr_tuple[1]
        else:
            get_ip_command = "vboxmanage guestproperty enumerate %s" % uuid
            get_ip_tuple = use_shell.shell(get_ip_command)
            ip_regex = re.compile(r'Net/0/V4/IP, value: (\S*),')
            ip_match = ip_regex.search(get_ip_tuple[0])
            time.sleep(10)
            while True:
                ip = random.randint(1, 254)
                ping_command = "ping 10.10.43.%s -c 1" % ip
                ping_result = use_shell.shell(ping_command)
                ping_regex = re.compile(r'(\d*)\sreceived')
                ping_match = ping_regex.search(ping_result[0])
                if ping_match.group(1) == 0:
                    change_network_command = "vboxmanage controlvm %s nic1 bridged eth1" % uuid
                    try:
                        use_shell.shell(change_network_command)
                        use_shell.shell("rm '/home/njuptcloud/VmManager/operation/interfaces'")
                    except:
                        print("hehe")

                    network_file = open('interfaces', 'a')
                    network_file.write('# The loopback network interfaces\n')
                    network_file.write('auto lo \n')
                    network_file.write('iface lo inet loopback\n')
                    network_file.write('# The primary network interface\n')
                    network_file.write('auto eth0\n')
                    network_file.write('iface eth0 inet static\n')
                    network_file.write('address 10.10.43.%s\n' % ip)
                    network_file.write('gateway 10.10.43.20\n')
                    network_file.write('netmask 255.255.255.0\n')
                    network_file.close()
                    host_path = '/home/njuptcloud/VmManager/operation/interfaces'
                    guest_path = '/etc/network/interfaces'
                    username = 'root'
                    passwd = 'root'
                    try:
                        use_shell.shell("vboxmanage guestcontrol %s copyto %s %s --username %s --password %s" % (host_path, guest_path, username, passwd))
                        use_shell.shell('vboxmanage guestcontrol %s exec --image /sbin/ifdown --username %s --password %s --wait-exit --wait-stdout -- eth0' % (uuid, username, passwd))
                        time.sleep(2)
                        use_shell.shell('vboxmanage guestcontrol %s exec --image /sbin/ifup --username %s --password %s --wait-exit --wait-stdout -- eth0' % (uuid, username, passwd))
                    except:
                        print('hehe2')

                    break
                else:
                    time.sleep(1)

            while True:
                get_ip_tuple = use_shell.shell(get_ip_command)
                ip_match = ip_regex.search(get_ip_tuple[0])
                if ip_match:
                    break
                else:
                    time.sleep(1)
            reply_dict["request_result"] = "success"
            reply_dict["vm_ip"] = ip_match.group(1)
            reply_dict["vm_username"] = "username"
    else:
        reply_dict["request_result"] = "request_error"
        reply_dict["error_information"] = "The virtual machine is already running"


def shutdown_vm(reply_dict):
    uuid = reply_dict["vm_uuid"]
    vm_state = get_vm_state(uuid)
    if (vm_state == 'running') or (vm_state == 'paused'):
        command = "vboxmanage controlvm %s acpipowerbutton" % uuid
        stdout_stderr_tuple = use_shell.shell(command)
        if stdout_stderr_tuple[1] != None:
            reply_dict["request_result"] = "execution_error"
            reply_dict["error_information"] = stdout_stderr_tuple[1]
        else:
            reply_dict["request_result"] = "success"
    else:
        reply_dict["request_result"] = "request_error"
        reply_dict["error_information"] = "Virtual machine in invalid state: %s" % vm_state


def savestate_vm(reply_dict):
    uuid = reply_dict["vm_uuid"]
    vm_state = get_vm_state(uuid)
    if (vm_state == 'running') or (vm_state == 'paused'):
        command = "vboxmanage controlvm %s savestate" % uuid
        stdout_stderr_tuple = use_shell.shell(command)
        if stdout_stderr_tuple[1] != None:
            reply_dict["request_result"] = "execution_error"
            reply_dict["error_information"] = stdout_stderr_tuple[1]
        else:
            reply_dict["request_result"] = "success"
    else:
        reply_dict["request_result"] = "request_error"
        reply_dict["error_information"] = "Virtual machine in invalid state: %s" % vm_state


def delete_vm(reply_dict):
    uuid = reply_dict["vm_uuid"]
    vm_state = get_vm_state(uuid)
    if (vm_state != 'running') and (vm_state != 'paused'):
        command = "vboxmanage unregistervm %s --delete" % uuid
        stdout_stderr_tuple = use_shell.shell(command)
        if stdout_stderr_tuple[1] != None:
            reply_dict["request_result"] = "execution_error"
            reply_dict["error_information"] = stdout_stderr_tuple[1]
        else:
            reply_dict["request_result"] = "success"
    else:
        reply_dict["request_result"] = "request_error"
        reply_dict["error_information"] = "Virtual machine in invalid state: %s" % vm_state


def control_vm(request):
    request_dict = eval(request)
    reply_dict = {"request_id": request_dict["request_id"], "request_type": request_dict["request_type"],
                  "request_userid": request_dict["request_userid"], "vm_name": request_dict["vm_name"],
                  "vm_uuid": request_dict["vm_uuid"]}

    control_type = request_dict["request_type"]
    if control_type == "start":
        start_vm(reply_dict)
    elif control_type == "shutdown":
        shutdown_vm(reply_dict)
    elif control_type == "savestate":
        savestate_vm(reply_dict)
    elif control_type == "delete":
        delete_vm(reply_dict)
    print(reply_dict)
    send_socket.send_reply(reply_dict)