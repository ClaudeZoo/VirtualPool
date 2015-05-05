__author__ = 'Claude'

import re
import use_shell
import send_socket


def start_vm(request):
    request_dict = eval(request)
    request_id = request_dict["request_id"]
    request_type = request_dict["request_type"]
    request_userid = request_dict["request_userid"]
    vm_name = request_dict["vm_name"]
    vm_uuid = request_dict["vm_uuid"]
    #check state
    command = "vboxmanage startvm %s --type headless" % vm_name
    start_vm_tuple = use_shell.shell(command)
    if start_vm_tuple[1] != None:
        error_information = {"request_id": request_id, "request_type": request_type, "request_userid": request_userid,
                             "request_result": "execution_error", "error_information": start_vm_tuple[1]}
        print error_information
        send_socket.send_reply(error_information)
    else:
        get_ip_command = "vboxmanage guestproperty enumerate %s" % vm_name
        get_ip_tuple = use_shell.shell(get_ip_command)
        ip_regex = re.compile(r'Net/0/V4/IP, value: (\S*),')
        ip_match = ip_regex.search(get_ip_tuple[0])
        success_information = {"request_id": request_id, "request_type": request_type, "user_id":request_userid, "request_result": "success", "vm_name":vm_name, "vm_uuid":vm_uuid,
        "vm_ip":ip_match.group(1), "vm_username": "hehe"}
        print success_information
        send_socket.send_reply(success_information)


def shutdown_vm(request):
    request_dict = eval(request)
    request_id = request_dict["request_id"]
    request_type = request_dict["request_type"]
    request_userid = request_dict["request_userid"]
    vm_name = request_dict["vm_name"]
    vm_uuid = request_dict["vm_uuid"]
    #check state
    command = "vboxmanage controlvm %s acpipowerbutton" % vm_name
    shutdown_vm_tuple = use_shell.shell(command)
    if shutdown_vm_tuple[1] != None:
        error_information = {"request_id": request_id, "request_type": request_type, "request_userid": request_userid,
                             "request_result": "execution_error", "error_information": shutdown_vm_tuple[1]}
        print error_information
        send_socket.send_reply(error_information)
    else:
        success_information = {"request_id": request_id, "request_type": request_type, "user_id":request_userid, "request_result": "success", "vm_name":vm_name, "vm_uuid":vm_uuid}
        send_socket.send_reply(success_information)


def savestate_vm(request):
    request_dict = eval(request)
    request_id = request_dict["request_id"]
    request_type = request_dict["request_type"]
    request_userid = request_dict["request_userid"]
    vm_name = request_dict["vm_name"]
    vm_uuid = request_dict["vm_uuid"]
    #check state
    command = "vboxmanage controlvm %s savestate" % vm_name
    savestate_vm_tuple = use_shell.shell(command)
    if savestate_vm_tuple[1] != None:
        error_information = {"request_id": request_id, "request_type": request_type, "request_userid": request_userid,
                             "request_result": "execution_error", "error_information": savestate_vm_tuple[1]}
        print error_information
        send_socket.send_reply(error_information)
    else:
        success_information = {"request_id": request_id, "request_type": request_type, "user_id":request_userid, "request_result": "success", "vm_name":vm_name, "vm_uuid":vm_uuid}
        send_socket.send_reply(success_information)


def delete_vm(request):
    request_dict = eval(request)
    request_id = request_dict["request_id"]
    request_type = request_dict["request_type"]
    request_userid = request_dict["request_userid"]
    vm_name = request_dict["vm_name"]
    vm_uuid = request_dict["vm_uuid"]
    #check state
    command = "vboxmanage unregistervm %s --delete" % vm_name
    delete_vm_tuple = use_shell.shell(command)
    if delete_vm_tuple[1] != None:
        error_information = {"request_id": request_id, "request_type": request_type, "request_userid": request_userid, "request_result": "execution_error", "error_information": delete_vm_tuple[1]}
        print error_information
        send_socket.send_reply(error_information)
    else:
        success_information = {"request_id": request_id, "request_type": request_type, "user_id":request_userid, "request_result": "success", "vm_name":vm_name, "vm_uuid":vm_uuid}
        send_socket.send_reply(success_information)


def control_vm(request):
    control_type = eval(request)["request_type"]
    if control_type == "start":
        start_vm(request)
    elif control_type == "shutdown":
        shutdown_vm(request)
    elif control_type == "savestate":
        savestate_vm(request)
    elif control_type == "delete":
        delete_vm(request)