# -*- coding: utf-8 -*-

import os
import socket
import threading
import time

from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip

import database


class MultiThread(object):
    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.db = database.MysqlClass()
        self.course = ''
        self.results = ''
        self.robot_port = 5400

    def listen(self):

        self.sock.listen(10)
        while True:
            client, address = self.sock.accept()
            client.settimeout(300)
            threading.Thread(args=(client, address), target=self.listen_to_client).start()

    def check_exsit(self, sid, file_path):
        path = 'record/'
        path_list = os.listdir(path)
        have_dir = False
        for iterm in path_list:
            if iterm == sid:
                have_dir = True
            else:
                pass
        if not have_dir:
            os.mkdir(path + sid, 0755)
            print('Dir not found! make new dir ' + sid)
        with open(file_path, 'wb') as f:
            pass

    def recv_image(self, client, filepath):
        while True:
            data = client.recv(8192)
            if not data:
                break
            else:
                with open(filepath, 'ab') as f:
                    f.write(data)
        print('data received')

    def save_image(self, client):
        client.send('Welcome from server!')
        print("receiving, please wait for a second ...")

        id_filename = client.recv(1024).split(';')
        sid = id_filename[0]
        filename = id_filename[1]
        path = 'record/' + sid + '/' + filename
        client.send('id get!')

        print('Begin to save ' + filename + ' ...')

        self.check_exsit(sid, path)
        t = threading.Thread(target=self.recv_image, args=(client, path))
        t.setDaemon(True)
        t.start()
        t.join()
        print('Finished saving ' + filename + ' ...')

    def merge_file(self, client):
        try:
            client.send('Welcome from server!')

            print("receiving, please wait for a second ...")

            id_filename = client.recv(1024).split(';')
            sid = id_filename[0]
            filename = id_filename[1]
            recording_time = id_filename[2]
            path = 'record/' + sid + '/' + filename
            client.send('id get!')

            print('merge file ' + filename)

            clip1 = AudioFileClip('record/' + sid + '/' + sid + recording_time + '-record.wav')
            clip2 = VideoFileClip('record/' + sid + '/' + sid + recording_time + '-video.avi')

            new_video = clip2.set_audio(clip1)
            new_video.write_videofile(path)

            client.send('merge success')

            print('merge succes!')

        except Exception as e:
            client.send('merge error')
            print(e)

    def listen_to_client(self, client, address):

        print('connect by: ', address)

        size = 2048
        link = True  # type: bool
        while link:
            try:
                data = client.recv(size)
                if data:
                    print(data.decode('utf-8'))

                    if data == '點名':
                        client.send('接收點名')
                        roll_call_course = client.recv(size)

                        self.course = roll_call_course.strip()
                        all_students = self.db.get_student_data(self.course)

                        while all_students == '':
                            time.sleep(1)
                            all_students = self.db.get_student_data(self.course)

                            print ('重新存取資料')

                        stu_names = str(all_students.encode('utf-8'))
                        client.send(stu_names)

                        print('傳送' + all_students)
                        link = False

                    elif data == '點名完畢':
                        client.send('接收成功')
                        roll_call_data = client.recv(size)
                        record_success = self.db.roll_call(roll_call_data, self.course)

                        if record_success:
                            print(roll_call_data, '出席紀錄成功')
                        link = False

                    elif data == '課堂作業':
                        classwork = self.db.get_classwork().encode('utf-8')
                        client.send(classwork)

                        print('作業:', classwork.decode('utf-8'))

                    elif data == '公告':
                        bulletin = self.db.get_bulletin().encode('utf-8')
                        client.send(bulletin)

                        print('公告:', bulletin.decode('utf-8'))
                        link = False

                    elif data == '所有課程':
                        class_names = self.db.get_class().encode('utf-8')
                        client.send(class_names)

                        print('課程:', class_names.decode('utf-8'))
                        link = False

                    elif data == '找課程':
                        client.send('ok')
                        course_name = client.recv(size)
                        if len(self.db.get_course_name(course_name)) > 0:
                            if isinstance(self.db.get_course_name(course_name), unicode):
                                response = self.db.get_course_name(course_name).encode('utf-8')
                            else:
                                response = self.db.get_course_name(course_name)
                        else:
                            response = '沒有課程'
                        client.send(response)
                        link = False

                    elif data == 'reading':
                        client.send('Which unit do you want to choose?')
                        reading_unit = client.recv(size)
                        reading_data = self.db.get_reading(reading_unit).encode('utf-8')
                        client.sendall(reading_data)
                        link = False

                    elif data == 'conversation':
                        client.send('Which unit do you want to choose?')
                        conversation_unit = client.recv(size)
                        conversation_character = self.db.get_conversation(conversation_unit).encode('utf-8')
                        client.send(conversation_character)
                        link = False

                    elif data == 'log':
                        client.send('please send log')
                        user_log = client.recv(8192)
                        record_success = self.db.student_conversation(user_log)

                        if record_success:
                            print('對話紀錄成功')
                            print(user_log)
                        link = False

                    elif data == 'get robot port':
                        print(self.robot_port)
                        client.send(str(self.robot_port))
                        link = False

                    elif data == 'get robot port(G)':
                        client.send(str(self.robot_port))
                        self.robot_port += 1
                        if self.robot_port >= 5500:
                            self.robot_port = 5400
                        link = False

                    elif data == 'file':
                        self.save_image(client)
                        link = False

                    elif data == 'merge':
                        self.merge_file(client)
                        link = False

                    elif data == 'account':
                        client.send('account')
                        teacher_account = client.recv(1024)
                        if self.db.get_account(teacher_account):
                            client.send('log in')
                        else:
                            client.send('no account')
                        link = False

                    else:
                        print(type(data), '傳送', data.decode('utf-8'))
                        client.sendall(data.decode('utf-8'))

                else:
                    time.sleep(1)
            except TypeError:
                client.close()
                return False

        client.close()


MultiThread('140.134.26.200', 5007).listen()
