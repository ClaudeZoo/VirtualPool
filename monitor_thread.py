# coding:utf-8
import SocketServer
from threading import Thread, Timer
from os import getcwd, path
from operation.use_shell import shell
from settings import MY_IP
from settings import MONITOR_PORT


class MonitorTCPHandler(SocketServer.BaseRequestHandler):

    thread_set = set()

    def handle(self):
        request_dict = eval(self.request.recv(1024).strip())
        if 'type' in request_dict and 'vm_uuid' in request_dict:
            if request_dict['type'] == "start":
                if 'vm_uuid' in request_dict:
                    log_thread = LogThread(request_dict['vm_uuid'])
                    self.thread_set.add(request_dict['vm_uuid'])
                    log_thread.start()
                    self.request.sendall(str(dict(result='success')))
            elif request_dict['type'] == "end":
                self.thread_set.remove()
                self.request.sendall(str(dict(result='success')))
            elif request_dict['type'] == "query":
                pass
            else:
                pass
        else:
            pass
        response_dict = dict(result="illegal")
        self.request.sendall(str(response_dict))


class MonitorThread(Thread):

    def __init__(self):
        super(MonitorThread, self).__init__()
        self.tcp_server = SocketServer.ThreadingTCPServer((MY_IP, MONITOR_PORT), MonitorTCPHandler)


class LogThread(Thread):

    def __init__(self, vm_uuid, thread_set):
        super(LogThread, self).__init__()
        self.vm_uuid = vm_uuid
        self.pid = get_vm_pid(vm_uuid)
        self.thread_set = thread_set
        self.log_file_name = path.join(getcwd(), '/var/log/virtualpool/%s-%s.txt' % (self.vm_uuid[:8], self.pid))
        self.command = 'cat /proc/%s/statm | cut -d ' ' -f 1,2,3,6 >> %s' % (self.pid, self.log_file_name)
        self.command_2 = 'cat /proc/%s/stat | cut -d ' ' -f 10,14,15 >> %s' % (self.pid, self.log_file_name)

    def run(self):
        while self.vm_uuid in self.thread_set:
            Timer(0.2, self.write_log())

    def write_log(self):
        shell(self.command)
        shell(self.command_2)


def get_vm_pid(uuid):
    command = "ps aux | grep %s | head -1 | awk '{print $2}'" % uuid
    pid_tuple = shell(command)
    if pid_tuple[0]:
        return int(pid_tuple[0])


class AnalyseThread(Thread):
    # 分析进程
    def __init__(self, vm_uuid):
        Thread.__init__(self)
        self.vm_uuid = vm_uuid
        self.pid = get_vm_pid(self.vm_uuid)

    def run(self):
        return None
