#!/usr/bin/python
# -*- coding: utf-8 -*-
#import pymysql
import threading
import MySQLdb
import functools
import time


def synchronized(wrapped):
    lock = threading.Lock()
    print(lock, id(lock))

    @functools.wraps(wrapped)
    def _wrap(*args, **kwargs):
        with lock:
            print("Calling '%s' with Lock %s from thread %s [%s]"
                  % (wrapped.__name__, id(lock),
                     threading.current_thread().name, time.time()))
            result = wrapped(*args, **kwargs)
            print("Done '%s' with Lock %s from thread %s [%s]\n"
                  % (wrapped.__name__, id(lock),
                     threading.current_thread().name, time.time()))
            return result

    return _wrap


class MysqlClass(object):
    def __init__(self):
        self.db = MySQLdb.connect("127.0.0.1", "user", "1234", "student", charset='utf8')
        self.cursor = self.db.cursor()

    def get_classwork(self):
        self.cursor.execute(
            "select content from classwork where classwork_id = (select max(classwork_id) from classwork);")
        classwork = self.cursor.fetchone()
        return classwork[0]

    def get_bulletin(self):
        self.cursor.execute("select content from bulletin_board where " + \
                            "bulletin_id = (select max(bulletin_id) from bulletin_board);")
        bulletin = self.cursor.fetchone()
        return bulletin[0]

    def get_class(self):
        self.cursor.execute("select course_name from course_information;")
        results = self.cursor.fetchall()
        class_names = ''
        for i in results:
            class_names += i[0] + ';'

        return class_names

    def get_course_name(self, course):
        course_data = course.split(',')

        sql = "SELECT course_name FROM course_information WHERE course_teacher = '{}' " \
              "and course_dayofweek = {} and course_starthour <= {} and course_endhour >= {}" \
            .format(course_data[0], course_data[1], course_data[2], course_data[2])

        self.cursor.execute(sql)
        results = self.cursor.fetchone()

        if results is not None:
            return results[0]
        else:

            return '目前沒有課程'

    def get_student_data(self, course):
        students = ''
        try:
            print('連接mysql')
            course_id = str(self.get_course_id(course))

            sql = "SELECT student_id,student_name FROM student_data ,practice_courses as p " + \
                  "WHERE student_id = p.stu_id and course_id = {};".format(course_id)

            self.cursor.execute(sql)

            results = self.cursor.fetchall()
            for i in results:
                students += i[0] + ' ' + i[1] + ';'

        except NameError:
            print("連線失敗", self.db.rollback())
        except TypeError:
            print('型態錯誤')

        return students

    @synchronized
    def roll_call(self, data, course):

        date = 'curdate()'
        attends = data[:-1]
        attends = attends.split(';')
        sql_sentence = ''
        course_id = self.get_course_id(course)
        for rollcall in attends:
            rollcall = rollcall.split()
            sql_sentence += "('{}','{}','{}','{}', {}),".format(rollcall[0], rollcall[1], course_id, rollcall[2], date)

        sql_sentence = sql_sentence[:-1]
        sql_sentence = "INSERT INTO roll_call(stu_id, stu_name, course_id , status, datetime) VALUES {};" \
            .format(sql_sentence)
        try:
            self.cursor.execute(sql_sentence)
            self.db.commit()
        except NameError:
            self.db.rollback()

        return True

    def get_course_id(self, course):

        sql = "SELECT course_id FROM course_information " + \
              "WHERE course_name = \"{}\";".format(course)

        self.cursor.execute(sql)
        results = self.cursor.fetchone()

        return results[0]

    def get_account(self, account):

        sql = "SELECT teacher_id FROM teacher_data " + \
              "WHERE teacher_id = \"{}\";".format(account)

        self.cursor.execute(sql)
        results = self.cursor.fetchone()

        if len(results) == 0:
            return False
        else:
            return True

    def get_word(self, unit):
        sql = "use essential_english_words_1;"
        self.cursor.execute(sql)
        sql = "SELECT word FROM words WHERE unit = {};".format(str(unit))
        self.cursor.execute(sql)
        words = ''
        results = self.cursor.fetchall()
        print(results)
        for res in results:
            words += res[0] + ";;"

        sql = "use student;"
        self.cursor.execute(sql)
        return words

    def get_reading(self, unit):
        sql = "use network;"
        self.cursor.execute(sql)
        sql = "SELECT content FROM reading WHERE unit = {};".format(str(unit))
        self.cursor.execute(sql)
        reading = ''
        results = self.cursor.fetchall()
        print(results)
        for res in results:
            reading += res[0] + ";;"

        sql = "use student;"
        self.cursor.execute(sql)
        return reading

    def get_conversation(self, unit):
        import json
        sql = "use network;"
        self.cursor.execute(sql)

        sql = "SELECT `order`, `character`, `content` FROM conversation WHERE unit = {};".format(str(unit))
        self.cursor.execute(sql)

        character = []
        order = []
        content = []
        conversation = {'order': [], 'characters': [], 'content': []}
        results = self.cursor.fetchall()
        for res in results:
            order.append(res[0])
            character.append(res[1])
            content.append(res[2])
        conversation['order'] = order
        conversation['characters'] = character
        conversation['content'] = content

        sql = "use student;"
        self.cursor.execute(sql)

        return json.dumps(conversation)

    def student_conversation(self, student_conversation_log):
        import json
        from jiwer import wer
        datetime = 'NOW()'
        conversation = json.loads(student_conversation_log)
        sql_sentence = ''
        sid = str(conversation['student'][0])
        character = str(conversation['character'][0])
        print(character)
        for i in range(len(conversation['student'])):
            stu_say = conversation['student_say'][i].replace("'", r"\'")
            chr_say = conversation['character_say'][i].replace("'", r"\'")
            word_error_rate = wer(str(chr_say), str(stu_say))
            sql_sentence += "('{}', '{}', '{}', '{}', {}, {})," \
                .format(sid, character, stu_say, chr_say, word_error_rate, datetime)

        sql_sentence = "INSERT INTO conversation_record(stu_id, character_name, stu_say, character_say , " + \
                       "word_error_rate, datetime) VALUES {};".format(sql_sentence[:-1])
        print(sql_sentence)
        try:
            self.cursor.execute(sql_sentence)
            self.db.commit()
        except NameError:
            self.db.rollback()

        return True
