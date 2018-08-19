# !/usr/bin/env python
# -*- coding: utf-8 -*-


import threading
import os
from socket import SOCK_STREAM, socket, AF_INET

SIZE = 1024


def check_file():
    list = os.listdir('.')
    for iterm in list:
        if iterm == 'image.jpg':
            os.remove(iterm)
            print('remove')
        else:
            pass


def tcp_link(sock, addr):
    print("Accept new connection from %s : %s..." % addr)
    sock.send(b'Welcome from server!')
    print("receiving, please wait for a second ...")
    while True:
        data = sock.recv(SIZE)
        if not data:
            print('reach the end of file')
            break
        elif data == 'begin to send':
            print('create file')
            check_file()
            with open('./image.jpg', 'wb') as f:
                pass
        else:
            with open('./image.jpg', 'ab') as f:
                f.write(data)
    sock.close()
    print('receive finished')
    print('Connection from %s:%s closed.' % addr)


s = socket(AF_INET, SOCK_STREAM)
s.bind(('140.134.26.200', 5007))
s.listen(1)
print('Waiting for connection...')

while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcp_link, args=(sock, addr))
    t.start()
