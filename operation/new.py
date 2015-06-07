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


def find_port():
    check_port_sql = "SELECT * FROM ports WHERE state='free' LIMIT 1"
    sql_result = mysql.execute_sql(check_port_sql)
    if sql_result.__len__() != 0:
        return sql_result[0]
    else:
        return 'empty'


def new_vm(request):
    request_dict = eval(request)
    reply_dict = {"request_id": request_dict["request_id"], "request_type": request_dict["request_type"],
                  "request_userid": request_dict["request_userid"]}
    new_vm_exec(reply_dict)
    print(reply_dict)
    send_socket.send_reply(reply_dict)

def new_vm_exec(reply_dict):
    port_info = find_port()
    if port_info != 'empty':
        port_number = port_info[1]
        new_vm_name = random_str()
        #check if there is a same virtual machine
        original_vm_name = 'ubuntu-sample'
        command = "vboxmanage clonevm %s --name %s --register" % (original_vm_name, new_vm_name)
        result_error_tuple = use_shell.shell(command)

        if result_error_tuple[1] != None:
            reply_dict["request_result"] = "execution_error"
            reply_dict["error_information"] = result_error_tuple[1]

        else:
            print(result_error_tuple[0])
            get_uuid_command = "vboxmanage showvminfo %s --machinereadable" % new_vm_name
            get_uuid_tuple = use_shell.shell(get_uuid_command)
            uuid_regex = re.compile(r'UUID="(\S*?)"')
            uuid_match = uuid_regex.search(get_uuid_tuple[0])
            uuid = uuid_match.group(1)
            shared_folder_path = "/Users/Claude/Desktop/empty"
            use_shell.shell('vboxmanage sharedfolder add %s --name %s --hostpath %s --readonly --automount' % (uuid, uuid ,shared_folder_path))
            use_shell.shell('vboxmanage modifyvm %s --natpf1 "guestssh,tcp,,%s,,22"' % (uuid, port_number))
            insert_sql = "INSERT INTO vm_user \
                          (vm_uuid, vm_name, vm_type, vm_userid) \
                          VALUES ('%s', '%s', '%s', '%s')" % \
                         (uuid, new_vm_name, "normal", reply_dict["request_userid"])
            result = mysql.execute_sql(insert_sql)
            if result == "error":
                mysql.execute_sql("UPDATE vm_user\
                                  SET vm_type='%s', vm_userid='%s'\
                                  WHERE vm_uuid='%s'" % ("normal", reply_dict["request_userid"], uuid))

            update_port_sql = "UPDATE ports \
                                SET state='%s', owner='%s'\
                                WHERE port='%s'" % ("occupied", new_vm_name, port_number)
            mysql.execute_sql(update_port_sql)

            reply_dict["request_result"] = "success"
            reply_dict["vm_name"] = new_vm_name
            reply_dict["vm_username"] = "ubuntu-user"
            reply_dict["vm_uuid"] = uuid_match.group(1)
            reply_dict["port"] = port_number

    else:
        reply_dict["request_result"] = "execution_error"
        reply_dict["error_information"] = "Run out of port"


if __name__ == '__main__':
    print("test")