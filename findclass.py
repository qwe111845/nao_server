# -*- coding: UTF-8 -*-
import socket
import database as d

import json
import database
import threading
import jiwer as wer




data = {"character_say": ["Well, I'm from Brighton, England. I like to surf, and\nI'm learning to fly small airplanes.\
I don't like to bake cupcakes."], "character": ["Nick"], "student_say": ["well I'm from flight Angela I like to Surf\
 and I'm learning to fly small airplanes I don't like to bake cupcakes"], "student": ["d0342273"]}

stu = d.MysqlClass()
stu.student_conversation(json.dumps(data))
print(json.dumps(data))
print(type(json.dumps(data)))
"""
m = d.MysqlClass()

print(m.get_bulletin())
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('192.168.0.113', 5555))

sock.listen(10)

def listen_to_client(client, address):

    print('connect by: ', address)
    size = 2048
    link = True  # type: bool
    while link:
        try:
            data = client.recv(size)
            if data:
                print(data.decode('utf-8'))
        except:
            break

while True:
    client, address = sock.accept()
    client.settimeout(300)
    threading.Thread(target=listen_to_client, args=(client, address)).start()




import speech_recognition as sr

# obtain path to "english.wav" in the same folder as this script
from os import path
AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "229-28.wav")

r = sr.Recognizer()
with sr.AudioFile(AUDIO_FILE) as source:
    audio = r.record(source)  # read the entire audio file
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio, language="zh-TW"))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

"""



