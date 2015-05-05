__author__ = 'Claude'

import re
import use_shell
import send_socket


def modify_vm(request):
    request_dict = eval(request)
    request_id = request_dict["request_id"]
    request_type = request_dict["request_type"]
    request_userid = request_dict["request_userid"]
    vm_name = request_dict["vm_name"]
    vm_uuid = request_dict["vm_uuid"]
    vm_property = request_dict["vm_property"]
    property_value = request_dict["property_value"]
    #check state
    if vm_property == "memory":
        command = "vboxmanage modifyvm %s --memory %s" % (vm_name, property_value)
        modify_tuple = use_shell.shell(command)
        if modify_tuple[1] == "None":
            error_information = {"request_id": request_id, "request_type": request_type, "request_userid": request_userid,
                             "request_result": "execution_error", "error_information": modify_tuple[1]}
            print error_information
            send_socket.send_reply(error_information)
        else:
            success_information = {"request_id": request_id, "request_type": request_type, "user_id":request_userid, "request_result": "success", "vm_name":vm_name, "vm_uuid":vm_uuid,
        "property": vm_property, "property_value": property_value}
            send_socket.send_reply(success_information)