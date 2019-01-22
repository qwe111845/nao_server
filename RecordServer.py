#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import socket, threading, os
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip


SIZE = 1024


def checkExsit(id, filepath):
    path = 'record/'
    list = os.listdir(path)
    havedir = False
    for iterm in list:
        if iterm == id:
            havedir = True
        else:
            pass
    if not havedir:
        os.mkdir(path + id, 0755)
        print('Dir not found! make new dir ' + id)
    with open(filepath, 'wb') as f:
        pass

def recvImage(sock, filepath):
    while True:
        data = sock.recv(512)
        if not data:
            break
        else:
            with open(filepath, 'ab') as f:
                f.write(data)
    print 'data received'


def saveImage(sock, id, filename, path):
    print 'Begin to save ' + filename + ' ...'
    checkExsit(id, path)
    t = threading.Thread(target=recvImage, args=(sock, path))
    t.setDaemon(True)
    t.start()
    t.join()
    print 'Finished saving ' + filename + ' ...'

def merge_file(sock, id, filename, path):
    try:
        print 'merge file ' + filename
        clip1 = AudioFileClip('record/' + id + '/' + id + '-record.wav')
        clip2 = VideoFileClip('record/' + id + '/' + id + '-video.avi')

        new_video = clip2.set_audio(clip1)
        new_video.write_videofile(path)

        sock.send('merge success')
        print 'merge succes!'
    except Exception as e:
        sock.send('merge error')
        print(e)


def tcplink(sock, addr):
    print("Accept new connection from %s : %s..." % addr)
    sock.send('Welcome from server!')
    print("receiving, please wait for a second ...")
    id_filename = sock.recv(SIZE).split(';')
    id = id_filename[0]
    filename = id_filename[1]
    path = 'record/' + id + '/' + filename
    sock.send('id get!')
    while True:
        recv = sock.recv(SIZE)
        if recv == 'c':
            print 'receive command'
            cmd = sock.recv(SIZE)
            print 'recv: %s' % cmd
            recv = None
        elif recv == 'f':
            print 'file command'
            saveImage(sock, id, filename, path)
            recv = None
        elif recv == 'merge':
            merge_file(sock, id, filename, path)
            recv = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('140.134.26.200', 5007))
s.listen(2)
print 'Waiting for connection...'
while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
