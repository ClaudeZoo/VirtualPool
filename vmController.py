#coding:utf-8
__author__ = 'Claude'

import operation.new
import operation.modify


def resolve_request(request):

    request_type = eval(request)["request_type"]
    if request_type == "new":
        operation.new.new_vm(request)
    else:
        print "type_error"
