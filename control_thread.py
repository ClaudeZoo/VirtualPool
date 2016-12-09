# coding:utf-8
import SocketServer
import threading
import Queue
from operationQueue import de_queue
from operation.control import control_vm
from operation.network import handle_network_request
from settings import MY_IP
from settings import CONTROL_PORT


class ControlTCPHandler(SocketServer.BaseRequestHandler):
    # 继承BaseRequestHandler类, 监听端口并处理请求
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
        if request_type == 'new':  # 根据请求类型来转发请求, 目前只有新建虚拟机(new)采用异步方式
            if request_user not in self.user_dict: # 如果当前没有该用户的队列
                self.user_dict[request_user] = Queue.Queue(maxsize=10)  # 每个用户最多同时执行20个新建请求
            if self.user_dict[request_user].full():
                response['request_response'] = "rejected"
                self.request.sendall(str(response))
            else:
                self.user_dict[request_user].put(data)  # 将请求加入队列
                response['request_response'] = "received"  # 回复iDashBoard,新建请求已收到
                self.request.sendall(str(response))
                if request_user not in self.running_queue_dict:
                    self.running_queue_dict[request_user] = "running"
                    if de_queue(self.user_dict[request_user]) == "done":  # 处理请求队列直至结束
                        del self.running_queue_dict[request_user]
                        del self.user_dict[request_user]
        elif request_type == 'network':
            handle_network_request(data_dict, response)
            self.request.sendall(str(response))
        else:
            request_vm_uuid = data_dict['vm_uuid']
            if request_vm_uuid in self.vm_set:  # 每台虚拟机只能同时执行一个请求
                response['request_result'] = "rejected"
                response['error_information'] = "An other operation is being executing"
            else:
                self.vm_set.add(request_vm_uuid)
                response = control_vm(data)  # 将请求转发给control_vm函数处理
                self.vm_set.remove(request_vm_uuid)
            self.request.sendall(str(response))


class ControlThread(threading.Thread):
    def __init__(self):
        super(ControlThread, self).__init__()
        self.tcp_server = SocketServer.ThreadingTCPServer((MY_IP, CONTROL_PORT), ControlTCPHandler)

    def run(self):
        self.tcp_server.serve_forever()
