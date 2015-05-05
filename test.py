__author__ = 'Claude'

import socket

HOST = '59.66.112.121'
PORT = 23333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
cmd = raw_input("Please input cmd:")
s.sendall(cmd)
data = s.recv(1024)
print data
s.close()