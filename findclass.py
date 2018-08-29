# -*- coding: utf-8 -*-

import time


import socket
import database
import time
""""
from datetime import datetime
b = database.MysqlClass()
a = datetime.now()

data = 't11122334,' + str(datetime.isoweekday(a)) + ',' + a.strftime("%H")

print (b.get_reading(1))

"""

port = 5007
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('140.134.26.200', port))
    s.send('reading')
    response = s.recv(2048)
    s.send('1')
    data = s.recv(8192)
    reading_data = data.split(';;')
    if reading_data[len(reading_data) - 1] == '':
        del reading_data[len(reading_data) - 1]

    print (reading_data)


finally:
    try:
        s.close() # activate output of the box
    except:
        pass


