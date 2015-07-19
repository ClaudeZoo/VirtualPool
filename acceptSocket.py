__author__ = 'Claude'

import SocketServer
import threading
import Queue
from operationQueue import de_queue
from operation.control import control_vm
from send_socket import send_reply

HOST = '127.0.0.1'
PORT = 23333
USER_DICT = dict()
VM_DICT = set()
RUNNING_QUEUE = dict()


class MyTCPHandler(SocketServer.BaseRequestHandler):
    
    def handle(self):

        data = self.request.recv(1024).strip()
        data_dict = eval(data)

        request_id = data_dict['request_id']
        request_type = data_dict['request_type']
        request_user = data_dict['request_userid']
        response = dict()
        response['request_id'] = request_id
        response['request_type'] = request_type
        response['request_userid'] = request_user
        if request_type == 'new' or request_type == 'delete':
            if request_user not in USER_DICT:
                USER_DICT[request_user] = Queue.Queue(maxsize=10)
            if USER_DICT[request_user].full():
                response['request_response'] = "rejected"
                self.request.sendall(str(response))
            else:
                USER_DICT[request_user].put(data)
                response['request_response'] = "received"
                self.request.sendall(str(response))
                if request_user not in RUNNING_QUEUE:
                    RUNNING_QUEUE[request_user] = "running"
                    if de_queue(USER_DICT[request_user]) == "done":
                        del RUNNING_QUEUE[request_user]
                        del USER_DICT[request_user]

        else:
            request_vm_uuid = data_dict['vm_uuid']
            if request_vm_uuid in VM_DICT:
                response['request_result'] = "rejected"
                response['error_information'] = "An other operation is being executing"
            else:
                VM_DICT.add(request_vm_uuid)
                response = control_vm(data)
                VM_DICT.remove(request_vm_uuid)
            self.request.sendall(str(response))



class ServerThread(threading.Thread):
    def run(self):
        server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
        server.serve_forever()


class PrintThread(threading.Thread):
    def run(self):
        print("hello world")


if __name__ == '__main__':
    thread1 = ServerThread()
    thread2 = PrintThread()
    thread1.start()
    thread2.start()