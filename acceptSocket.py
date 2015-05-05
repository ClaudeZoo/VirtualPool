__author__ = 'Claude'

import SocketServer
import re
import Queue
import operationQueue

HOST = '101.5.209.97'
PORT = 23333
USER_DICT = dict()
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
                if operationQueue.de_queue(USER_DICT[request_user]) == "done":
                    del RUNNING_QUEUE[request_user]
                    del USER_DICT[request_user]


def start_server():
    server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()


if __name__ == '__main__':
    start_server()