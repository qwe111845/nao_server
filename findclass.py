# -*- coding: UTF-8 -*-



#transcribe_gcs("gs://speech_to_text_class/d0342273 2019-03-07 17'58-record wav")

from jiwer import wer
avg_confidence = 4.1154165416846434685461465463541854
print float('%.4f' % avg_confidence)
import database as db
a = db.MysqlClass()
b,c,d = a.get_reading_content('d0342273')
print(b)

speak1 = "the laboratory Mia's father had a laboratory but she had no idea what was in it or dad always closed " \
         "and locked the door when she knew that he used it to do projects for work you never told me I what " \
         "these projects were one night me approach the door to the laboratory she stopped and thought I wonder " \
         "what crazy experiment he is doing now suddenly she heard a loud noise it sounded like an evil laugh " \
         "the noise scared her so she walked quickly the next night her friend Liz came to her house when this " \
         "arrived Mia told her about the night before it was terrible she said why don't we see what is in " \
         "their lives asked it will be a fun adventure Mia felt nervous about going into her father's laboratory " \
         "but she agreed as always the door was locked they waited until me his father left the laboratory to " \
         "eat dinner he didn't lock the door I said let's go for Tori was dark the girls walk down the stairs " \
         "carefully Mia smelled strange chemicals what terrible thing was creating suddenly they heard an evil " \
         "laugh it was even worse than the one me I heard the night before what if a monster was going to kill " \
         "them I had to do something she shouted for help me as father ran into the room and turned on the lights " \
         "he said you must have learned my secret to kill us me a sad monster the more need this for your birthday " \
         "I wanted to give it to you then you can have it now I hope you like it"


speak = "the first peacock Argos lived in ancient Greece he was a husband and a proud father he worked hard and did well at his job but one thing about him wasn't normal he was born with 100 eyes having many eyes was usually a benefit to him he had a chance to see many things also since he was very good at guarding things while sleeping he only rested a few days at a time the other stayed awake for Hera a Great Goddess is primary function was to guard a special cow the cow was very important to her it was her favorite that the most essential part of his job was to keep the cow loan it had to be kept separate from all the other cows and far away from people this was an easy job for Argos the cow just ate grass all day but the god Zeus wanted the cow he wanted to take it away from Harrah he had a plan he found a great music player he asked the man to play a beautiful song for Argos Zeus was certain Argos would go to sleep the song had an immediate effect Argos couldn't focus on his job he fell asleep Zeus saw this and he took the cow Sarah was very angry with our Gus she turned him into a peacock she put his many eyes on his tail Argos was very sad Zeus on how much trouble it caused Argos he made another plan he turned our goes into a group of stars he wanted our goes to remain in the sky forever even today about the site where all his problems began we can still see him in the night sky"
truth = "The First Peacock Argos lived in Ancient Greece He was a husband and a proud father He worked hard and did well at his job But one thing about him wasn't normal He was born with 100 eyes Having many eyes was usually a benefit to him He had a chance to see many things Also since he had so many eyes he was very good at guarding things While sleeping he only rested a few eyes at a time The others stayed awake He worked for Hera a great goddess His primary function was to guard a special cow The Cow was very important to Hera It was her favorite pet The most essential part of his job was to keep the cow alone It had to be kept separate from all the other cows and far away from people This was an easy job for Argos The cow just ate grass all day But the god Zeus wanted the cow He wanted to take it away from Hera He had a plan He found a great music player He asked the man to play a beautiful song for Argos Zeus was certain Argos would go to sleep The song had an immediate effect Argos couldn't focus on his job He fell asleep Zeus saw this and he took the cow Hera was very angry with Argos She turned him into a peacock She put his many eyes on his tail Argos was very sad Zeus saw how much trouble he had caused Argos He made another plan He turned Argos into a group of stars He wanted Argos to remain in the sky forever Even today Argos' image remains there above the site where all his problems began We can still see him in the night sky"

print(1-wer(truth, speak))

"""
def transcribe_file(speech_file):
    from google cloud import speech
    from google cloud speech import enums
    from google cloud speech import types
    client = speech SpeechClient()

    r = sr Recognizer()
    with io open(speech_file 'rb') as audio_file:
        content = audio_file read()

    audio = types RecognitionAudio(content=content)
    config = types RecognitionConfig(
        encoding=enums RecognitionConfig AudioEncoding LINEAR16,
        sample_rate_hertz=48000,
        audio_channel_count=4,
        language_code='zh-TW')

    response = client recognize(config audio)
    # Each result is for a consecutive portion of the audio  Iterate through
    # them to get the transcripts for the entire audio file 
    for result in response results:
        # The first alternative is the most likely one for this portion 
        print(u'Transcript: {}' format(result alternatives[0] transcript))


def setchannel(file_path):
    import numpy as np
    sameple_rate music_data = wavfile read(file_path)
    left = []
    right = []
    front = []
    back = []
    for item in music_data:
        left append(item[0])
        right append(item[1])
        front append(item[2])
        back append(item[3])


    wavfile write('left wav' sameple_rate np array(left))
    wavfile write('right wav' sameple_rate np array(right))
    wavfile write('front wav' sameple_rate np array(right))
    wavfile write('back wav' sameple_rate np array(right))

transcribe_file("record/d0342273/d0342273 2019-02-28 16'30-record wav")
#transcribe_file("right wav")
setchannel("record/d0342273/d0342273 2019-02-28 16'30-record wav")



import wave
import numpy as np
import matplotlib pyplot as plt
filepath = "record/d0342273/d0342273-record wav"  # 添加路径
f = wave open(filepath 'rb')

params = f getparams()
nchannels sampwidth framerate nframes = params[:4]
strData = f readframes(nframes)  # 读取音频，字符串格式
waveData = np fromstring(strData dtype=np int16)
waveData = waveData * 1 0 / (max(abs(waveData)))  # wave幅值归一化
waveData = np reshape(waveData [nframes nchannels])

f close()
# plot the wave
time = np arange(0 nframes) * (1 0 / framerate)

print((1 0 * nframes)/(1 0 * framerate))

plt figure()
plt subplot(5 1 1)
plt plot(time waveData[: 0])
plt xlabel("Time(s)")
plt ylabel("Amplitude")
plt title("Ch-1 wavedata")
plt grid('on')  # 标尺，on：有，off:无。
plt subplot(5 1 3)
plt plot(time waveData[: 1])
plt xlabel("Time(s)")
plt ylabel("Amplitude")
plt title("Ch-2 wavedata")
plt grid('on')  # 标尺，on：有，off:无。
plt subplot(5 1 5)
plt plot(time waveData[: 1])
plt xlabel("Time(s)")
plt ylabel("Amplitude")
plt title("Ch-3 wavedata")
plt grid('on')  # 标尺，on：有，off:无。
plt show()

"""





