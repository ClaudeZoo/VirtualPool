__author__ = 'Claude'

import SocketServer
import threading
import Queue
from operationQueue import de_queue
from operation.control import control_vm
from settings import MY_ADDRESS
from settings import MY_PORT


class MyTCPHandler(SocketServer.BaseRequestHandler):
    vm_set = set()
    user_dict = dict()
    running_queue_dict = dict()

    def handle(self):

        data = self.request.recv(1024).strip()
        data_dict = eval(data)
        response = dict()
        response['request_id'] = data_dict['request_id']
        request_type = data_dict['request_type']
        request_user = data_dict['request_userid']
        response['request_type'] = request_type
        response['request_userid'] = request_user
        if request_type == 'new':
            if request_user not in self.user_dict:
                self.user_dict[request_user] = Queue.Queue(maxsize=20)
            if self.user_dict[request_user].full():
                response['request_response'] = "rejected"
                self.request.sendall(str(response))
            else:
                self.user_dict[request_user].put(data)
                response['request_response'] = "received"
                self.request.sendall(str(response))
                if request_user not in self.running_queue_dict:
                    self.running_queue_dict[request_user] = "running"
                    if de_queue(self.user_dict[request_user]) == "done":
                        del self.running_queue_dict[request_user]
                        del self.user_dict[request_user]
        else:
            request_vm_uuid = data_dict['vm_uuid']
            if request_vm_uuid in self.vm_set:
                response['request_result'] = "rejected"
                response['error_information'] = "An other operation is being executing"
            else:
                self.vm_set.add(request_vm_uuid)
                response = control_vm(data)
                self.vm_set.remove(request_vm_uuid)
            self.request.sendall(str(response))


class ServerThread(threading.Thread):
    def run(self):
        server = SocketServer.ThreadingTCPServer((MY_ADDRESS, MY_PORT), MyTCPHandler)
        server.serve_forever()


class PrintThread(threading.Thread):
    def run(self):
        print("hello world")


if __name__ == '__main__':
    thread1 = ServerThread()
    thread2 = PrintThread()
    thread1.start()
    thread2.start()
