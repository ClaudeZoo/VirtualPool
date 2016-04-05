# coding:utf-8
import SocketServer
import pickle
import numpy as np
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from threading import Thread, Timer
from os import getcwd, path
from operation.use_shell import shell
from settings import MY_IP, MONITOR_PORT, MODAL_NAME


class MonitorTCPHandler(SocketServer.BaseRequestHandler):

    thread_set = set()

    def handle(self):
        request_dict = eval(self.request.recv(1024).strip())
        if 'type' in request_dict and 'vm_uuid' in request_dict:
            print request_dict
            if request_dict['type'] == "start":
                if 'vm_uuid' in request_dict:
                    self.thread_set.add(request_dict['vm_uuid'])
                    self.pid = get_vm_pid(request_dict['vm_uuid'])
                    log_thread = LogThread(request_dict['vm_uuid'], self.thread_set, self.pid)
                    log_thread.start()
                    
            elif request_dict['type'] == "end":
                self.thread_set.remove(request_dict['vm_uuid'])
                self.request.sendall(str(dict(result='success')))
            elif request_dict['type'] == "query":
                if 'vm_uuid' in request_dict:
                    if path.exists(MODAL_NAME):
                        model_file = file(MODAL_NAME, "rb")
                        model_str = pickle.load(model_file)
                        neural_network = pickle.loads(model_str)
                    else:
                        neural_network = {}
                    if neural_network != {}:
                        data_file_name = '%s-%s.txt' % (request_dict['vm_uuid'][:8], get_vm_pid(request_dict['vm_uuid']))
                        print data_file_name
                        if path.exists(data_file_name):
                            data_file = np.loadtxt(data_file_name, int)
                            last_line_data = data_file[-1]
                            print last_line_data
                            result = neural_network.activate(last_line_data)
                            self.request.sendall(str(dict(result='success', process=result[0])))
                        else:
                            self.request.sendall(str(dict(result='cannot find the log.')))
                    else:
                        self.request.sendall(str(dict(result='model file not found')))
                else:
                    self.request.sendall(str(dict(result='Invalid request')))
            else:
                response_dict = dict(result="Invalid type")
                self.request.sendall(str(response_dict))
        else:
            response_dict = dict(result="illegal")
            self.request.sendall(str(response_dict))


class MonitorThread(Thread):

    def __init__(self):
        super(MonitorThread, self).__init__()
        self.tcp_server = SocketServer.ThreadingTCPServer((MY_IP, MONITOR_PORT), MonitorTCPHandler)

    def run(self):
        self.tcp_server.serve_forever()


class LogThread(Thread):

    def __init__(self, vm_uuid, thread_set, pid):
        super(LogThread, self).__init__()
        self.vm_uuid = vm_uuid
        self.pid = pid
        self.thread_set = thread_set
        self.log_file_name = path.join(getcwd(), '%s-%s.txt' % (self.vm_uuid[:8], self.pid))
        self.command = 'cat /proc/%s/statm | cut -d " " -f 1,2,3,6' % self.pid
        self.command_2 = 'cat /proc/%s/stat | cut -d " " -f 10,14,15' % self.pid

    def run(self):
        while self.vm_uuid in self.thread_set:
            Timer(0.1, self.write_log).run()

    def write_log(self):
        data = shell(self.command)[0].strip('\n') + ' ' + shell(self.command_2)[0].strip('\n')
        shell('echo %s >> %s' % (data, self.log_file_name))


def get_vm_pid(uuid):
    command = "ps aux | grep %s | head -1 | awk '{print $2}'" % uuid
    pid_tuple = shell(command)
    if pid_tuple[0]:
        return int(pid_tuple[0])


class AnalyseThread(Thread):
    # 分析进程
    def __init__(self, neural_network, data, request):
        Thread.__init__(self)
        self.neural_network = neural_network
        self.data = data
        self.handle_request = request

    def run(self):
        print 1
        result = self.neural_network.predict(self.data)
        print 2
        self.handle_request.sendall(str(dict(result='success', process=result[0][0])))
