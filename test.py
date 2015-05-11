__author__ = 'Claude'

import socket


HOST = '101.5.98.70'
PORT = 23333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
#cmd = raw_input("Please input cmd:")
cmd = {"request_id": "123", "request_type": "new", "request_userid": "3"}
s.sendall(str(cmd))
data = s.recv(1024)
print data
s.close()