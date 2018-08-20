# -*- coding: utf-8 -*-
import socket
import database
import time
from datetime import datetime
b = database.MysqlClass()
a = datetime.now()

data = 't11122334,' + str(datetime.isoweekday(a)) + ',' + a.strftime("%H")

print (b.get_course_name(data))


"""
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('140.134.26.200', port))
    s.send(str('點名'))

    class_data = s.recv(2048)
    if class_data == '接收點名':
        p = '英語會話'
        s.sendall(p)
        class_data = ''

        class_data = s.recv(4096)
        id = 0
        while class_data == '' and id < 5:
            time.sleep(1.5)
            class_data = s.recv(4096)
            print ('等')
            id = id +1

        print (class_data)
finally:
    try:
        s.close()
    except:
        pass
"""