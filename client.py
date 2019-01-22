#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket

SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('140.134.26.200', 5007))
s.send('file')
print s.recv(SIZE)
s.send('d0342273;d0342273-record.wav')
print s.recv(SIZE)
print ('sending, please wait for a second ...')
with open('./ip.mp3', 'rb') as f:
    for data in f:
        s.send(data)
print ('sended !')
s.close()
print ('connection closed')

