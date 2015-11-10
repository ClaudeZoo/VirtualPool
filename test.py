#coding:utf-8
__author__ = 'Claude'
import socket
#测试文件
#可模拟iDashBoard发送消息来测试VmManager

HOST = '127.0.0.1'
PORT = 23333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
#cmd = raw_input("Please input cmd:")
cmd_start = {"request_id": "123", "request_type": "start", "request_userid": "3", "vm_name": "", "vm_uuid": ""}
cmd = {"request_id": "123", "request_type": "new", "request_userid": "3"}
s.sendall(str(cmd))
data = s.recv(1024)
print data
s.close()
