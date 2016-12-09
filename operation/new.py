# coding:utf-8
import re
import string
import random
from operation.use_shell import shell
from operation.modify import modify_vm_memory
from settings import *
import send_socket


def random_str(random_length=8):  # 获取8位随机虚拟机名字
    return ''.join(random.sample(string.ascii_letters + string.digits, random_length))


def new_vm(request):
    # 处理新建虚拟机请求,准备需要返回的基本数据
    request_dict = eval(request)
    reply_dict = {"request_id": request_dict["request_id"], "request_type": request_dict["request_type"],
                  "request_userid": request_dict["request_userid"], "port": request_dict["port"],
                  "request_memory": request_dict["request_memory"]}
    new_vm_exec(reply_dict)
    print(reply_dict)
    send_socket.send_reply(reply_dict)


def new_vm_exec(reply_dict):
    new_vm_name = random_str()
    # check if there is a same virtual machine
    original_vm_name = 'ubuntu-sample'
    command = "vboxmanage clonevm %s --name %s --register" % (original_vm_name, new_vm_name)
    result_error_tuple = shell(command)

    if result_error_tuple[1]:  # 如果返回错误结果
        reply_dict["request_result"] = EXECUTION_ERROR
        reply_dict["error_information"] = result_error_tuple[1]

    else:
        modify_vm_memory(new_vm_name, reply_dict['request_memory'])
        get_uuid_command = "vboxmanage showvminfo %s --machinereadable" % new_vm_name
        get_uuid_tuple = shell(get_uuid_command)
        uuid_regex = re.compile(r'UUID="(\S*?)"')
        uuid_match = uuid_regex.search(get_uuid_tuple[0])
        uuid = uuid_match.group(1)
        folder_path = path.join(getcwd(), 'empty')
        port = reply_dict["port"]
        # 获取虚拟机的uuid并在虚拟机内新建一个同名文件夹,便于iDashBoard Client获取uuid
        shell('vboxmanage sharedfolder add %s --name %s --hostpath %s --readonly --automount'
              % (uuid, uuid, folder_path))
        shell('vboxmanage modifyvm %s --natpf1 "guestssh,tcp,,%s,,22"' % (uuid, port))
        shell('vboxmanage modifyvm %s --uart1 0x3F8 4 --uartmode1 file %s%s.log' % (uuid, LOG_PATH, uuid))
        reply_dict["request_result"] = RESULT_SUCCESS
        reply_dict["vm_name"] = new_vm_name
        reply_dict["vm_username"] = "ubuntu-user"
        reply_dict["vm_uuid"] = uuid_match.group(1)


if __name__ == '__main__':
    shell('vboxmanage sharedfolder add ubuntu-sample --name hehe --hostpath ./empty --readonly --automount')
