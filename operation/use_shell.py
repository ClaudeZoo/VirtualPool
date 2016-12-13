# coding:utf-8
import subprocess
from settings import GUEST_OS_ADMIN, GUEST_OS_PASSWD


def shell(command):  # 执行脚本 返回脚本的返回值
    s = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    return s.communicate()


def guest_shell(vm_name, bin_path, command):
    host_command = "vboxmanage guestcontrol %s run --exe %s --username %s --password %s -- %s" \
                   % (vm_name, bin_path, GUEST_OS_ADMIN, GUEST_OS_PASSWD, command)
    return shell(host_command)
