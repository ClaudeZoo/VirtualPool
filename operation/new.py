__author__ = 'Claude'

import re
from operation.use_shell import shell
import send_socket
from random import Random
from os import getcwd
from os import path
from mysql import execute_sql


def random_str(random_length=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


def find_port():
    check_port_sql = "SELECT * FROM ports WHERE state='free' LIMIT 1"
    sql_result = execute_sql(check_port_sql)
    if sql_result.__len__() != 0:
        return sql_result[0]
    else:
        return 'empty'


def new_vm(request):
    request_dict = eval(request)
    reply_dict = {"request_id": request_dict["request_id"], "request_type": request_dict["request_type"],
                  "request_userid": request_dict["request_userid"], "port": request_dict["port"]}
    new_vm_exec(reply_dict)
    print(reply_dict)
    send_socket.send_reply(reply_dict)


def new_vm_exec(reply_dict):
    new_vm_name = random_str()
    #check if there is a same virtual machine
    original_vm_name = 'ubuntu-sample'
    command = "vboxmanage clonevm %s --name %s --register" % (original_vm_name, new_vm_name)
    result_error_tuple = shell(command)

    if result_error_tuple[1] != None:
        reply_dict["request_result"] = "execution_error"
        reply_dict["error_information"] = result_error_tuple[1]

    else:
        print(result_error_tuple[0])
        get_uuid_command = "vboxmanage showvminfo %s --machinereadable" % new_vm_name
        get_uuid_tuple = shell(get_uuid_command)
        uuid_regex = re.compile(r'UUID="(\S*?)"')
        uuid_match = uuid_regex.search(get_uuid_tuple[0])
        uuid = uuid_match.group(1)
        folder_path = path.join(getcwd(), 'empty')
        port = reply_dict["port"]
        shell('vboxmanage sharedfolder add %s --name %s --hostpath %s --readonly --automount' % (uuid, uuid, folder_path))
        shell('vboxmanage modifyvm %s --natpf1 "guestssh,tcp,,%s,,22"' % (uuid, port))
        reply_dict["request_result"] = "success"
        reply_dict["vm_name"] = new_vm_name
        reply_dict["vm_username"] = "ubuntu-user"
        reply_dict["vm_uuid"] = uuid_match.group(1)
        

if __name__ == '__main__':
    shell('vboxmanage sharedfolder add ubuntu-sample --name hehe --hostpath ./empty --readonly --automount')
