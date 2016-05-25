# coding:utf-8
import SocketServer
import pickle
import numpy as np
import os
import re
from threading import Thread, Timer
from os import getcwd, path
from operation.use_shell import shell
from settings import MY_IP, MONITOR_PORT, LOG_PATH


re.compile(r"\[.*\]")


def analyse_log(uuid):
    log = open(log_name(uuid))
    lines = log.readlines()
    if len(lines) > 2:
        info = lines[-2]
    else:
        info = ""
    log.close()
    return len(lines), info


def log_file_exist(uuid):
    if path.exists(log_name(uuid)):
        return True
    else:
        return False


def log_name(uuid):
    return LOG_PATH + uuid + '.log'


class MonitorTCPHandler(SocketServer.BaseRequestHandler):

    thread_set = set()

    def handle(self):
        request_dict = eval(self.request.recv(1024).strip())
        if 'type' in request_dict and 'vm_uuid' in request_dict:
            print request_dict
            uuid = request_dict['vm_uuid']
            if request_dict['type'] == 'query':
                if log_file_exist(uuid):
                    rate, info = analyse_log(uuid)
                    if rate == 0:
                        self.request.sendall(str(dict(result='success', state='pre_kernel')))
                    else:
                        self.request.sendall(str(dict(result='success', state='kernel', rate=rate, info=info)))
            elif request_dict['type'] == 'stop':
                if log_file_exist(uuid):
                    os.remove(log_name(uuid))
                    self.request.sendall(str(dict(result='success')))
                else:
                    self.request.sendall(str(dict(result='failed')))
            else:
                self.request.sendall(str(dict(result='illegal')))


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
        self.log_file_name = path.join(getcwd(), '%s-%s' % (self.vm_uuid[:8], self.pid))
        self.command = 'cat /proc/%s/statm | cut -d " " -f 1,2,3,6' % self.pid
        self.command_2 = 'cat /proc/%s/stat | cut -d " " -f 10,14,15' % self.pid

    def run(self):
        while self.vm_uuid in self.thread_set:
            Timer(0.1, self.write_log).run()
        #os.remove(self.log_file_name)

    def write_log(self):
        data_str = shell(self.command)[0].strip('\n') + ' ' + shell(self.command_2)[0].strip('\n')
        data_str_list = data_str.split()
        if os.path.isfile(self.log_file_name):
            log = open(self.log_file_name, 'r')
            first_data_str_list = log.readline().split()
            log.close()
            data = ""
            for i in range(len(data_str_list)):
                data += (str(int(data_str_list[i]) - int(first_data_str_list[i])) + " ")
            shell('echo %s >> %s' % (data, self.log_file_name))
        else:
            shell('echo %s >> %s' % (data_str, self.log_file_name))


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
