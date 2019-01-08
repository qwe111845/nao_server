#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket

SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('140.134.26.203', 5007))

s.send('enter room')
link = True
while link != False:
    data = raw_input()
    s.send(data)

    print(s.recv(1024))

s.close()
print ('connection closed')

