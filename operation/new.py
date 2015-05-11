__author__ = 'Claude'

import re
import use_shell
import send_socket
from random import Random
import mysql

def random_str(random_length=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str

def new_vm(request):
    request_dict = eval(request)
    request_id = request_dict["request_id"]
    request_type = request_dict["request_type"]
    user_id = request_dict["request_userid"]
    new_vm_name = random_str()
    #check if there is a same virtual machine
    original_vm_name = 'ubuntu-server'
    command = "vboxmanage clonevm %s --name %s --register" % (original_vm_name, new_vm_name)

    result_error_tuple = use_shell.shell(command)

    if result_error_tuple[1] != None:
        error_information = {"request_id": request_id, "request_type": request_type, "request_userid": user_id,
                             "request_result": "execution_error", "error_information": result_error_tuple[1]}
        send_socket.send_reply(error_information)
    else:
        print(result_error_tuple[0])
        get_uuid_command = "vboxmanage showvminfo %s --machinereadable" % new_vm_name
        get_uuid_tuple = use_shell.shell(get_uuid_command)
        uuid_regex = re.compile(r'UUID="(\S*?)"')
        uuid_match = uuid_regex.search(get_uuid_tuple[0])
        uuid = uuid_match.group(1)
        #print("success")
        insert_sql = "INSERT INTO vm_user \
                      (vm_uuid, vm_name, vm_type, vm_userid) \
                      VALUES ('%s', '%s', '%s', '%s')" % \
                     (uuid, new_vm_name, "normal", user_id)
        result = mysql.execute_sql(insert_sql)
        if result == "error":
            mysql.execute_sql("UPDATE vm_user\
                              SET vm_type='%s', vm_userid='%s'\
                              WHERE vm_uuid='%s'" % ("normal", user_id, uuid))

        success_information = {"request_id": request_id, "request_type": request_type, "request_userid": user_id,
                               "vm_name": new_vm_name, "request_result": "success", "vm_username": "thucloud",
                               "vm_uuid": uuid_match.group(1)}
        #print success_information
        #send_socket.send_reply(success_information)

