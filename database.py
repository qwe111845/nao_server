# -*- coding: utf-8 -*-
# import pymysql
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
        sql = "select content from bulletin_board where bulletin_id = (" \
              "select max(bulletin_id) from bulletin_board);"
        self.cursor.execute(sql)
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
        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)

        results = self.cursor.fetchone()

        if results is not None:
            return results[0]
        else:
            return '目前沒有課程'

    def get_student_data(self, course):
        students = ''
        print(course)

        print('連接mysql')
        course_id = str(self.get_course_id(course))
        print(course_id)
        sql = "SELECT student_id,student_name FROM student_data ,practice_courses as p " + \
              "WHERE student_id = p.stu_id and course_id = {};".format(course_id)

        try:
            self.cursor.execute(sql)
        except NameError:
            print("連線失敗", self.db.rollback())
        except TypeError:
            print('型態錯誤')
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)

        results = self.cursor.fetchall()
        for i in results:
            students += i[0] + ' ' + i[1] + ';'

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
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql_sentence)
            self.db.commit()

        return True

    def get_course_id(self, course):

        sql = "SELECT course_id FROM student.course_information " + \
              "WHERE course_name = \"{}\";".format(course)

        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)

        results = self.cursor.fetchone()

        return results[0]

    def get_teacher_account(self, account):

        sql = "SELECT teacher_id FROM teacher_data " + \
              "WHERE teacher_id = \"{}\";".format(account)

        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)
        results = self.cursor.fetchone()

        if len(results) == 0:
            return False
        else:
            return True

    def get_student_account(self, account):

        sql = "SELECT * FROM essential_english_words_1.unit WHERE unit_id = (SELECT" + \
              " current_course FROM student.course_progress WHERE sid = \"{}\");".format(account)
        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
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

    def update_progress(self, data):
        stu_data = data.split(';')
        student = stu_data[0]
        course = stu_data[1]

        sql = "UPDATE student.course_progress SET current_course = {} WHERE sid = \"{}\";".format(course, student)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)
            self.db.commit()

    def get_word(self, unit):

        sql = "SELECT word FROM essential_english_words_1.words WHERE unit = " \
              "(SELECT unit FROM essential_english_words_1.unit WHERE" + \
              " unit_id = {});".format(str(unit))
        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)

        words = ''
        results = self.cursor.fetchall()
        print(results)
        for res in results:
            words += res[0] + ";;"

        return words

    def get_reading(self, unit):

        sql = "SELECT content FROM network.reading WHERE unit = {};".format(str(unit))
        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)
        reading = ''
        results = self.cursor.fetchall()
        print(results)
        for res in results:
            reading += res[0] + ";;"

        return reading

    def get_quiz(self, unit):

        import json
        sql = "SELECT q.`order`, q.answer, q.quiz, a.content FROM essential_english_words_1.unit_quiz AS q," \
              "essential_english_words_1.unit_answer AS a WHERE	q.unit = {} AND a.unit = {}	AND " \
              "a.`q_order` = q.`order`  AND q.answer = a.answer;".format(str(unit), str(unit))

        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)

        order = []
        answer = []
        quizes = []
        content = []

        quiz = {'order': [], 'answer': [], 'quiz': [], 'content': []}
        results = self.cursor.fetchall()

        for res in results:
            order.append(res[0])
            answer.append(res[1])
            quizes.append(res[2])
            content.append(res[3])

        quiz['order'] = order
        quiz['answer'] = answer
        quiz['quiz'] = quizes
        quiz['content'] = content

        return json.dumps(quiz)

    def get_conversation(self, unit):
        import json

        sql = "SELECT `order`, `character`, `content` FROM network.conversation WHERE unit = {};".format(str(unit))
        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
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

        return json.dumps(conversation)

    def student_conversation(self, student_conversation_log):
        import json
        from jiwer import wer
        datetime = 'NOW()'
        conversation = json.loads(student_conversation_log)
        sql_sentence = ''
        sid = str(conversation['student'][0])
        character = str(conversation['character'][0])
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
        except NameError, MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql_sentence)
            self.db.commit()

        return True

    def record_quiz_answer(self, student_reading_log):
        import json
        import MailTransfer
        datetime = 'NOW()'
        reading_log = json.loads(student_reading_log)
        sql_sentence = ''
        sid = str(reading_log['sid'])
        unit = str(reading_log['unit'])

        for i in range(len(reading_log['order'])):
            stu_r_ans = reading_log['stu_read_ans'][i].replace("'", r"\'")
            stu_ans = reading_log['stu_answer'][i]
            order = reading_log['order'][i]
            wer = reading_log['wer'][i]
            speed = reading_log['reading_speed'][i]
            sql_sentence += "('{}', '{}', '{}', '{}', '{}', '{}', {}, {})," \
                .format(sid, unit, order, stu_ans, stu_r_ans, wer, speed, datetime)

        sql_sentence = "INSERT INTO `student`.`stu_reading_answer` (`sid`, `unit`, `order`, `stu_answer`, " \
                       "`stu_read_ans`, `wer`, `reading_speed`, `reading_time`) VALUES {};".format(sql_sentence[:-1])
        try:
            self.cursor.execute(sql_sentence)
            self.db.commit()
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql_sentence)
            self.db.commit()
            return False

        MailTransfer.send_mail(sid)

        return True

    def get_reading_content(self, sid):
        sql = "select unit, content from essential_english_words_1.reading_content where rid = (select " \
              "current_course FROM student.course_progress where sid = '{}');".format(str(sid))
        try:
            self.cursor.execute(sql)
        except MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)
        results = self.cursor.fetchone()
        reading_len = len(results[1].split(' '))
        return int(results[0]), reading_len, results[1]

    def record_reading(self, sid, unit, content, speed, wer, confidence):

        datetime = 'NOW()'
        sql = "INSERT INTO `student`.`stu_reading_wer`(sid, unit, stu_reading_content, stu_reading_speed, " \
              "stu_reading_wer, avg_confidence, datetime) VALUE ('{}', {}, \"{}\", {}, {}, {},{});".\
            format(sid, unit, content, speed, wer, confidence, datetime)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except NameError, MySQLdb.OperationalError:
            self.operation_error()
            self.cursor.execute(sql)
            self.db.commit()
            return False

        return True

    def operation_error(self):
        self.db = MySQLdb.connect("127.0.0.1", "user", "1234", "student", charset='utf8')
        self.cursor = self.db.cursor()
