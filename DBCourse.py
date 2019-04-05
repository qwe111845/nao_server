#!/usr/bin/python
# -*- coding: utf-8 -*-
# import pymysql
import threading
import MySQLdb
import functools
import time
import database as db


class DBCourse(db.MysqlClass):

    def __init__(self):
        super(DBCourse, self).__init__()

    def get_teacher_account(self, account):

        sql = "SELECT teacher_id, teacher_name FROM teacher_data " + \
              "WHERE teacher_id = \"{}\";".format(account)

        self.cursor.execute(sql)
        results = self.cursor.fetchone()

        if len(results) == 0:
            return 'no account'
        else:
            return results[1].encode('utf-8')

    def get_student_account(self, account):

        sql = "SELECT * FROM course_3565.lesson WHERE lesson_id = (SELECT" + \
              " current_course FROM student.course_progress WHERE sid = \"{}\");".format(account)
        self.cursor.execute(sql)
        results = self.cursor.fetchone()

        if len(results) == 0:
            return 'no account'
        else:
            stu_data = ''
            for i in results:
                stu_data += str(i) + ';'

            stu_data = stu_data[:-1]
            return stu_data

    def get_word(self, lesson):

        sql = "SELECT word FROM course_3565.words WHERE lesson = (SELECT lesson FROM course_3565.lesson WHERE" + \
              " lesson = {});".format(str(lesson))
        self.cursor.execute(sql)

        words = ''
        results = self.cursor.fetchall()
        for res in results:
            words += res[0] + ";;"

        return words
