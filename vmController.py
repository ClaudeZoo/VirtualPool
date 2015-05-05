__author__ = 'Claude'

import time
import re
import operation.new
import operation.control
import operation.modify


def resolve_request(request):
    #time.sleep(10)

    request_type = eval(request)["request_type"]
    if request_type == "new":
        operation.new.new_vm(request)
    elif request_type == "modify":
        operation.modify.modify_vm(request)
    elif ((request_type == "start") or (request_type == "shutdown")
          or (request_type == "savestate") or (request_type == "delete")):
        operation.control.control_vm(request)
    else:
        print "type_error"