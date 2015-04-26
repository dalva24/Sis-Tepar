#!/usr/bin/env python

import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 2421
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send('{"method":"killserver","magicString":"q34tAq34tb3qy4IUaXa4t"}'.encode('utf-8'))
data = s.recv(BUFFER_SIZE)
s.close()

print ("received data:", data)