__author__ = 'Claude'

import mysql
import time
import operation.use_shell
import re
import datetime


def update():
    starttime = datetime.datetime.now()
    command = "vboxmanage list vms"
    return_tuple = operation.use_shell.shell(command)
    vm_regex = re.compile(r'"(.*?)"\s*\{(.*?)\}')
    for match in vm_regex.finditer(return_tuple[0]):
        result = mysql.execute_sql("SELECT * FROM vm_user \
                          WHERE vm_uuid = '%s'" % (match.group(2)))
        if result == ():
            mysql.execute_sql("INSERT INTO vm_user \
                      (vm_name, vm_uuid, vm_type) \
                      VALUES ('%s', '%s', '%s')" % (match.group(1), match.group(2), "nouser"))

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


    endtime = datetime.datetime.now()
    print (endtime - starttime).seconds
    #for line in results:


if __name__ == '__main__':
    while True:
        update()
        time.sleep(100)