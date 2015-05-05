__author__ = 'Claude'

import vmController


def de_queue(request_queue):
    while request_queue.qsize > 0:
        request = request_queue.get()
        vmController.resolve_request(request)
        print request
    return "done"