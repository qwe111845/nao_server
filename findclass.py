# -*- coding: UTF-8 -*-



#transcribe_gcs("gs://speech_to_text_class/d0342273 2019-03-07 17'58-record.wav")


import DBCourse
a = DBCourse.DBCourse()
a.get_word('1')
"""
def transcribe_file(speech_file):
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    r = sr.Recognizer()
    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        audio_channel_count=4,
        language_code='zh-TW')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))


def setchannel(file_path):
    import numpy as np
    sameple_rate, music_data = wavfile.read(file_path)
    left = []
    right = []
    front = []
    back = []
    for item in music_data:
        left.append(item[0])
        right.append(item[1])
        front.append(item[2])
        back.append(item[3])


    wavfile.write('left.wav', sameple_rate, np.array(left))
    wavfile.write('right.wav', sameple_rate, np.array(right))
    wavfile.write('front.wav', sameple_rate, np.array(right))
    wavfile.write('back.wav', sameple_rate, np.array(right))

transcribe_file("record/d0342273/d0342273 2019-02-28 16'30-record.wav")
#transcribe_file("right.wav")
setchannel("record/d0342273/d0342273 2019-02-28 16'30-record.wav")



import wave
import numpy as np
import matplotlib.pyplot as plt
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

print((1.0 * nframes)/(1.0 * framerate))

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

"""





