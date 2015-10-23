__author__ = 'Claude'

import time
import re
import operation.new
from operation.control import control_vm
import operation.modify


def resolve_request(request):
    #time.sleep(10)

    request_type = eval(request)["request_type"]
    if request_type == "new":
        operation.new.new_vm(request)
    elif request_type == "modify":
        operation.modify.modify_vm(request)
    else:
        print "type_error"