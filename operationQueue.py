__author__ = 'Claude'

from vmController import resolve_request


def de_queue(request_queue):
    while request_queue.qsize > 0:
        request = request_queue.get()
        resolve_request(request)
        print request
    return "done"