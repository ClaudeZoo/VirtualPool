# coding:utf-8
import re
from use_shell import shell
import time
from settings import *


def get_vm_state(uuid):
    state_tuple = shell("vboxmanage showvminfo %s --machinereadable" % uuid)
    state_re = re.compile(r'VMState="(.*?)"')
    match = state_re.search(state_tuple[0])
    if match:
        return match.group(1)


def execute_command(command, reply_dict):
    std_tuple = shell(command)
    if std_tuple[1] != None:
        reply_dict["request_result"] = EXECUTION_ERROR
        reply_dict["error_information"] = std_tuple[1]
    else:
        reply_dict["request_result"] = RESULT_SUCCESS


def start_vm(reply_dict):
    # 启动虚拟机
    uuid = reply_dict["vm_uuid"]
    vm_state = get_vm_state(uuid)
    if (vm_state != 'running') and (vm_state != 'paused'):
        command = "vboxmanage startvm %s " % uuid  # --type headless
        stdout_stderr_tuple = shell(command)
        if stdout_stderr_tuple[1]:
            reply_dict["request_result"] = EXECUTION_ERROR
            reply_dict["error_information"] = stdout_stderr_tuple[1]
        else:
            reply_dict["request_result"] = RESULT_SUCCESS
    else:
        reply_dict["request_result"] = REQUEST_ERROR
        reply_dict["error_information"] = "The virtual machine is already running"


def start_end_vm(reply_dict):
    uuid = reply_dict["vm_uuid"]
    get_ip_command = "vboxmanage guestproperty enumerate %s" % uuid
    get_ip_tuple = shell(get_ip_command)
    ip_regex = re.compile(r'Net/0/V4/IP, value: (\S*),')
    ip_match = ip_regex.search(get_ip_tuple[0])
    while True:
        get_ip_tuple = shell(get_ip_command)
        ip_match = ip_regex.search(get_ip_tuple[0])
        if ip_match:
            break
        else:
            time.sleep(1)
    reply_dict["request_result"] = RESULT_SUCCESS
    reply_dict["vm_ip"] = ip_match.group(1)
    reply_dict["vm_username"] = "username"


def shutdown_vm(reply_dict):
    # 关闭虚拟机
    uuid = reply_dict["vm_uuid"]
    vm_state = get_vm_state(uuid)
    if (vm_state == 'running') or (vm_state == 'paused'):
        command = "vboxmanage controlvm %s acpipowerbutton" % uuid
        execute_command(command, reply_dict)
    else:
        reply_dict["request_result"] = REQUEST_ERROR
        reply_dict["error_information"] = "Virtual machine in invalid state: %s" % vm_state


def savestate_vm(reply_dict):
    # 休眠虚拟机
    uuid = reply_dict["vm_uuid"]
    vm_state = get_vm_state(uuid)
    if (vm_state == 'running') or (vm_state == 'paused'):
        command = "vboxmanage controlvm %s savestate" % uuid
        execute_command(command, reply_dict)
    else:
        reply_dict["request_result"] = REQUEST_ERROR
        reply_dict["error_information"] = "Virtual machine in invalid state: %s" % vm_state


def add_nat_rule(reply_dict):
    # 添加nat规则
    uuid = reply_dict["vm_uuid"]
    host_port = reply_dict["host_port"]
    guest_port = reply_dict["guest_port"]
    protocol = reply_dict["protocol"]
    rule_name = str(host_port) + protocol + str(guest_port)
    command = "vboxmanage controlvm %s natpf1 %s,%s,,%s,,%s" % (uuid, rule_name, protocol, host_port, guest_port)
    execute_command(command, reply_dict)


def delete_nat_rule(reply_dict):
    # to do
    uuid = reply_dict["vm_uuid"]
    rule_name = reply_dict["rule_name"]


def delete_vm(reply_dict):
    uuid = reply_dict["vm_uuid"]
    vm_state = get_vm_state(uuid)
    if (vm_state != 'running') and (vm_state != 'paused'):
        command = "vboxmanage unregistervm %s --delete" % uuid
        execute_command(command, reply_dict)
    else:
        reply_dict["request_result"] = REQUEST_ERROR
        reply_dict["error_information"] = "Virtual machine in invalid state: %s" % vm_state


def control_vm(request):
    reply_dict = eval(request)
    control_type = reply_dict["request_type"]
    if control_type == "start":
        start_vm(reply_dict)
    elif control_type == "start_end":
        start_end_vm(reply_dict)
    elif control_type == "shutdown":
        shutdown_vm(reply_dict)
        time.sleep(2)
    elif control_type == "savestate":
        savestate_vm(reply_dict)
    elif control_type == "add_nat_rule":
        add_nat_rule(reply_dict)
    elif control_type == "delete_nat_rule":
        delete_nat_rule(reply_dict)
    elif control_type == "delete":
        delete_vm(reply_dict)
    print(reply_dict)
    return reply_dict
