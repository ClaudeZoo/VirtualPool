# coding: utf-8
import re
from use_shell import shell, guest_shell
from settings import *

INTNET = "intnet"

IFUP_PATH = "/sbin/ifup"
IFDOWN_PATH = "/sbin/ifdown"

IF_FILES = [path.join(BASE_PATH, "0", "interfaces"), path.join(BASE_PATH, "1", "interfaces"),
            path.join(BASE_PATH, "2", "interfaces"), path.join(BASE_PATH, "3", "interfaces"),
            path.join(BASE_PATH, "4", "interfaces"), path.join(BASE_PATH, "5", "interfaces"),
            path.join(BASE_PATH, "6", "interfaces"), path.join(BASE_PATH, "7", "interfaces")]

IF_NAMES = ["eth0", "eth1", "eth2", "eth3"]


def create_intnet(name, ip, netmask, lower_ip, upper_ip):
    command = "vboxmanage dhcpserver add --netname %s --ip %s --netmask %s --lowerip %s --upperip %s  --enable" \
              % (name, ip, netmask, lower_ip, upper_ip)
    return shell(command)


def delete_intnet(name):
    command = "vboxmanage dhcpserver remove --netname %s" % name
    return shell(command)


def add_vm_to_intnet(vm_name, if_no, if_code, net_name):
    command = "vboxmanage controlvm %s nic%s intnet %s" % (vm_name, if_no + 1, net_name)
    # if_no + 1 的原因：nic1 对应 eth0, nic2 对应 eth1，以此类推
    shell(command)
    replace_interface_file(vm_name, IF_FILES[if_code])
    return guest_shell(vm_name, IFUP_PATH, "ifup %s" % IF_NAMES[if_no])


def remove_vm_from_network(vm_name, if_no, if_code):
    guest_shell(vm_name, IFDOWN_PATH, "ifdown %s" % IF_NAMES[if_no])
    replace_interface_file(vm_name, IF_FILES[if_code])
    command = "vboxmanage controlvm %s nic%s null" % (vm_name, if_no + 1)
    return shell(command)


def create_hostonlyif(ip, netmask, lower_ip, upper_ip):
    command = "vboxmanage hostonlyif create"
    result_error_tuple = shell(command)
    if not result_error_tuple[1]:
        match_obj = re.search(r"Interface '(.*)' .*", result_error_tuple[0])
        if_name = match_obj.group(1)
        if if_name:
            command = "vboxmanage dhcpserver add --ifname %s --ip %s --netmask %s --lowerip %s --upperip %s  --enable" \
                      % (if_name, ip, netmask, lower_ip, upper_ip)
            result_error_tuple = shell(command)
            if not result_error_tuple[1]:
                result_error_tuple = if_name, None
            return result_error_tuple
        else:
            return None, "Regex Error"
    else:
        return result_error_tuple


def delete_hostonlyif(name):
    command = "vboxmanage dhcpserver remove --ifname %s" % name
    shell(command)
    command = "vboxmanage hostonlyif remove %s" % name
    return shell(command)


def add_vm_to_hostonlyif(vm_name, if_no, if_code, net_name):
    command = "vboxmanage controlvm %s nic%s hostonly %s" % (vm_name, if_no + 1, net_name)
    shell(command)
    replace_interface_file(vm_name, IF_FILES[if_code])
    return guest_shell(vm_name, IFUP_PATH, "ifup %s" % IF_NAMES[if_no])


def replace_interface_file(vm_name, if_file):
    command = "vboxmanage guestcontrol %s  copyto %s  /etc/network/interfaces --username %s --password %s" \
              % (vm_name, if_file, GUEST_OS_ADMIN, GUEST_OS_PASSWD)
    return shell(command)


def handle_network_request(data_dict, response_dict):
    print(data_dict)
    operation_type = data_dict["operation_type"]
    if operation_type == CREATE_INTNET:
        result_error_tuple = create_intnet(data_dict["net_name"], data_dict["ip"], data_dict["netmask"],
                                        data_dict["lower_ip"], data_dict["upper_ip"])
    elif operation_type == DELETE_INTNET:
        result_error_tuple = delete_intnet(data_dict["net_name"])
    elif operation_type == ADD_VM_TO_INTNET:
        result_error_tuple = add_vm_to_intnet(data_dict["vm_name"], data_dict["if_no"], data_dict["if_code"],
                                              data_dict["net_name"])

    elif operation_type == CREATE_HOSTONLY:
        result_error_tuple = create_hostonlyif(data_dict["ip"], data_dict["netmask"], data_dict["lower_ip"],
                                               data_dict["upper_ip"])
        response_dict["net_name"] = result_error_tuple[0]
    elif operation_type == DELETE_HOSTONLY:
        result_error_tuple = delete_hostonlyif(data_dict["name"])
    elif operation_type == ADD_VM_TO_HOSTONLY:
        result_error_tuple = add_vm_to_hostonlyif(data_dict["vm_name"], data_dict["if_no"], data_dict["if_code"],
                                                  data_dict["net_name"])
    elif operation_type == REMOVE_VM_FROM_NETWORK:
        result_error_tuple = remove_vm_from_network(data_dict["vm_name"], data_dict["if_no"], data_dict["if_code"])
    else:
        result_error_tuple = None, "Invalid Network Request Type"

    if result_error_tuple[1]:
        response_dict["request_result"] = EXECUTION_ERROR
        response_dict["error_information"] = result_error_tuple[1]
    else:
        response_dict["request_result"] = RESULT_SUCCESS


"""
if __name__ == '__main__':
    add_intnet("test_net_1", "192.168.123.0", "255.255.255.0", "192.168.123.2", "192.168.123.100")
    add_vm_to_intnet("ubuntu-sample", 1, 4, "test_net_1")
    remove_vm_from_network("ubuntu-sample", 1, 0)
    delete_intnet("test_net_1")
"""
