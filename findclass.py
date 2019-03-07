# -*- coding: UTF-8 -*-


import database as db

a = '00000000'
print(a)
"""

filepath = "record/d0342273/d0342273-record.wav"  # 添加路径
f = wave.open(filepath, 'rb')

params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
strData = f.readframes(nframes)  # 读取音频，字符串格式
waveData = np.fromstring(strData, dtype=np.int16)
waveData = waveData * 1.0 / (max(abs(waveData)))  # wave幅值归一化
waveData = np.reshape(waveData, [nframes, nchannels])

f.close()
# plot the wave
time = np.arange(0, nframes) * (1.0 / framerate)
plt.figure()
plt.subplot(5, 1, 1)
plt.plot(time, waveData[:, 0])
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title("Ch-1 wavedata")
plt.grid('on')  # 标尺，on：有，off:无。
plt.subplot(5, 1, 3)
plt.plot(time, waveData[:, 1])
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title("Ch-2 wavedata")
plt.grid('on')  # 标尺，on：有，off:无。
plt.subplot(5, 1, 5)
plt.plot(time, waveData[:, 1])
plt.xlabel("Time(s)")
plt.ylabel("Amplitude")
plt.title("Ch-3 wavedata")
plt.grid('on')  # 标尺，on：有，off:无。
plt.show()


data = {'character_say': ["I want to welcome Nick Carpenter to our staff meeting.We're so glad to have you on " + \
                          "our team, Nick. Let's all introduce ourselves.", 'And what do you like to do in your free time?', 'Thanks, Lucy. What about you. Nick ?'], 'character': ['Rose', 'Rose', 'Rose'], 'student_say': ["I want to welcome Nick comforter to our staff meeting we are so glad to have you on our team make let's all introduce ourselves", 'and hot do you like to do in your free time', 'sex Lucy heart about unique'], 'student': ['m0626957', 'm0626957', 'm0626957']}

stu = d.MysqlClass()
stu.student_conversation(json.dumps(data))
print(json.dumps(data))
print(type(json.dumps(data)))


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



