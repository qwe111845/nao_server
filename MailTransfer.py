# coding:utf8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import MailDB as db


def send_mail(sid):
    mail_host = 'smtp.gmail.com'
    mail_user = 'd0342273@mail.fcu.edu.tw'
    mail_pass = '[Myth]-apollo'
    mail_db = db.DBMail()
    port = 587
    me = mail_user
    msg = MIMEMultipart()
    unit, email_address = mail_db.get_mail(sid)
    msg['Subject'] = '課文辨識成果 單元' + str(unit)
    msg['From'] = me
    send_list = [email_address]

    mail_db.get_mail(sid)
    stu_reading_content, stu_reading_speed, stu_reading_wer, avg_confidence = mail_db.get_record_data(sid, unit)
    order, stu_answer, stu_read_ans, wer, reading_speed = mail_db.get_answer_data(sid, unit)

    ans_data = str()
    for i in range(4):

        ans_data += """ 
        <tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        </tr>
        """.format(unit, order[i], stu_answer[i], stu_read_ans[i], wer[i], reading_speed[i])

    html = """
<div id="container">
  <p><strong>課程錄音資料</strong></p>
  <div>
      <p>UNIT:<br />
      {}</p>
      <p style="max-width: 500px">CONTENT:<br />
      {}</p>
      <p>Reading speed(words/minute):<br />
      {}</p>
      <p>Reading wer(課文比對正確率)(%):
      <br />{}</p>
      <p>Average confidence:
      <br />{}</p>
  </div>
  
  <p><strong>會話測驗列表</strong></p>
  <div id="content">
   <table width="500" border="2" bordercolor="red" cellspacing="2">
  <tr>
    <td><strong>單元</strong></td>
    <td><strong>第幾題</strong></td>
    <td><strong>您的答案</strong></td>
    <td><strong>您的回答</strong></td>
    <td><strong>正確率</strong></td>
    <td><strong>朗讀語速</strong></td>
  </tr>
  """.format(unit, stu_reading_content, stu_reading_speed, stu_reading_wer, avg_confidence) + ans_data + """
</table>
  <p style="max-width: 400px"><strong><br />註:信心度為google語音模型對於辨識結果正確的信心程度，正常要在
                                            0.9以上才比較準，語音模型通常要唸得比較完整才能辨識成功，所以
                                            盡量唸完整正確率相對才會高
                                      <br />對了 機器人很笨常常聽錯，會話測驗答案有問題在跟我講
  </strong></p> 
  </div>
        """
    context = MIMEText(html, _subtype='html', _charset='utf-8')
    msg.attach(context)
    try:
        send_smtp = smtplib.SMTP()
        send_smtp.connect(mail_host, port)
        send_smtp.ehlo()
        send_smtp.starttls()
        send_smtp.ehlo()
        send_smtp.login(mail_user, mail_pass)
        send_smtp.sendmail(me, send_list, msg.as_string())
        send_smtp.close()
        return True
    except Exception, e:
        print str(e)
        return False

"""
if __name__ == '__main__':

    if send_mail('d0459838', 5):
        print("Send mail succed!")
    else:
        print("Send mail failed!")
"""