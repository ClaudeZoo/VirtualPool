# coding:utf-8
import mysql
import time
import operation.use_shell
import re


def update():  # 暂时废弃的功能
    command = "vboxmanage list vms"
    return_tuple = operation.use_shell.shell(command)
    vm_regex = re.compile(r'"(.*?)"\s*\{(.*?)\}')

    # 将数据库中没有的虚拟机加入到数据库
    for match in vm_regex.finditer(return_tuple[0]):
        result = mysql.execute_sql("SELECT * FROM vm_user \
                          WHERE vm_uuid = '%s'" % (match.group(2)))
        if result == ():
            mysql.execute_sql("INSERT INTO vm_user \
                      (vm_name, vm_uuid, vm_type) \
                      VALUES ('%s', '%s', '%s')" % (match.group(1), match.group(2), "nouser"))

    # 删除数据库中已经失效的虚拟机
    vm_list = mysql.execute_sql("SELECT * FROM vm_user")
    for line in vm_list:
        match = re.search(line[0], return_tuple[0])
        if not match:
            mysql.execute_sql("DELETE FROM vm_user \
                              WHERE vm_uuid = '%s'" % (line[0]))
        else:
            vminfo_tuple = operation.use_shell.shell("vboxmanage showvminfo %s --machinereadable" % (line[0]))
            match = re.search(r'macaddress1="(.*?)"', vminfo_tuple[0])
            print match.group(1)


if __name__ == '__main__':
    while True:
        update()
        time.sleep(100)