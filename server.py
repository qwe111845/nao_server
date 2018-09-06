# !/usr/bin/env python
# -*- coding: utf-8 -*-


import threading
import os
from socket import SOCK_STREAM, socket, AF_INET

SIZE = 1024


def check_file(id):
    path = 'record/'
    list = os.listdir(path)
    havedir = False
    for iterm in list:
        if iterm == id:
            print('have dir' + id)
            havedir = True
        else:
            pass
    if not havedir:
        os.mkdir(path + id, 0755)
        print('make dir ' + id)


def tcp_link(sock, addr):
    print("Accept new connection from %s : %s..." % addr)
    sock.send(b'Welcome from server!')
    print("receiving, please wait for a second ...")
    id_filename = sock.recv(SIZE).split(';')
    id = id_filename[0]
    filename = id_filename[1]
    path = 'record/' + id + '/' + filename
    sock.send('id get!')
    while True:
        data = sock.recv(SIZE)
        if not data:
            print('reach the end of file')
            break
        elif data == 'begin to send':
            print('create file ' + filename)
            check_file(id)
            with open(path, 'wb') as f:
                pass
        else:
            with open(path, 'ab') as f:
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
