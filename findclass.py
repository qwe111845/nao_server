# -*- coding: UTF-8 -*-
# !/usr/bin/env python
import socket
import json

utt = 'apple#banana#cherry#orange'
print(utt.split('# ;'))
port = 5007
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('140.134.26.200', port))
    s.send('conversation')
    response = s.recv(2048)
    print (response)
    s.send(str(1))
    conversation_data = s.recv(1024)
    print (conversation_data)
    conversation_dic = json.loads(conversation_data)

    characters = ''
    choose_sentence = 'The characters that can be selected are '
    characters_list = set(conversation_dic['characters'])
    for i in characters_list:
            characters += str(i) + ';'
            choose_sentence += str(i) + ' '
    characters = characters[:-1]
    choose_sentence = choose_sentence[:-1]
    print(characters)
    print(choose_sentence)
    characters = ''
    for i in conversation_dic['characters']:
        characters += str(i) + ';'

    characters = characters[:-1]


finally:
    try:
        s.close()
    except:
        pass

"""
SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('140.134.26.200', 5007))
print s.recv(SIZE)
s.send('d0342273;d0342273555.mp3')
print s.recv(SIZE)
s.send('f')
print 'sending, please wait for a second ...'
with open('./ip.mp3', 'rb') as f:
    for data in f:
        s.send(data)
print 'sended !'
s.close()
print 'connection closed'


SIZE = 1024

import os
import comtypes.client
path_to_ppt = "C:\Users\lin\Desktop\支援課堂助理機器人之課程教學發展.pptx"
path_to_folder = "C:\Users\lin\Desktop"
def export_presentation(path_to_ppt, path_to_folder):
  if not (os.path.isfile(path_to_ppt) and os.path.isdir(path_to_folder)):
    raise "Please give valid paths!"
  powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
  # Needed for script to work, though I don't see any reason why...
  powerpoint.Visible = True
  powerpoint.Open(path_to_ppt)
  # Or some other image types
  powerpoint.ActivePresentation.Export(path_to_folder, "JPG")
  #Presentation.Slides[1].Export("C:/path/to/jpg.jpg","JPG",800,600);
  powerpoint.Presentations[1].Close()
  powerpoint.Quit()






port = 5007
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('140.134.26.200', port))
    s.send('找課程')
    isok = s.recv(2048)
    currentTime = d.datetime.now()
    course_data = 't2223344' + ',' + str(d.datetime.isoweekday(currentTime)) \
                  + ',' + currentTime.strftime('%H')
    print course_data
    if isok == 'ok':
        s.send(course_data)

    class_name = s.recv(2048)
    print class_name

finally:
    try:
        s.close()
    except:
        pass

"""


