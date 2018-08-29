# -*- coding: utf-8 -*-

import socket
import database
import threading
import time


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

        # print 'Server waiting , port: ', self.port

    def listen(self):

        self.sock.listen(10)
        while True:
            client, address = self.sock.accept()
            client.settimeout(300)
            threading.Thread(args=(client, address), target=self.listen_to_client).start()

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
                        client.sendall('接收點名')
                        roll_call_course = client.recv(size)

                        self.course = roll_call_course.strip()
                        print(self.course)

                        all_students = self.db.link_mysql(self.course)

                        while all_students == '':
                            time.sleep(1)
                            all_students = self.db.link_mysql(self.course)
                            print ('重新存取資料')

                        stu_names = str(all_students.encode('utf-8'))
                        client.send(stu_names)

                        print(u'傳送' + all_students)

                    elif data == '點名完畢':
                        client.send('接收成功')

                        print('傳送 接收成功')

                        roll_call_data = client.recv(size)
                        ok = self.db.roll_call(roll_call_data, self.course)

                        if ok:
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
                    elif data == '所有課程':
                        class_names = self.db.get_class().encode('utf-8')
                        client.send(class_names)
                        print('課程:', class_names.decode('utf-8'))
                    elif data == '找課程':
                        client.send('ok')
                        course_name = client.recv(size)
                        response = self.db.get_course_name(course_name).encode('utf-8')
                        print (response)
                        client.send(response)
                    elif data == 'reading':
                        client.send('Which unit do you want to choose?')
                        reading_unit = client.recv(size)
                        reading_data = self.db.get_reading(reading_unit).encode('utf-8')
                        client.sendall(reading_data)
                        link = False
                    else:
                        print(type(data), '傳送', data.decode('utf-8'))
                        client.sendall(data.decode('utf-8'))
                else:
                    time.sleep(1)
            except TypeError:
                client.close()
                return False


MultiThread('140.134.26.200', 5007).listen()
