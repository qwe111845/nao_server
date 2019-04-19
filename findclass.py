# -*- coding: UTF-8 -*-




from jiwer import wer

speak = "Jones daughter was that bad. He fights people drinking and Joe had a great concerned about is it was not appropriate weight for a dog to behave as rent in the village west always spend the doctor by then the news about John Starks pray through the village of the paper wanted to go to John's house and try to instruct the dog to behave but it never will he try to be patient and taste the Teletubby count that also didn't work and to punish the dog how will I stay out of my dog's bad habit by himselfjust friend came to talk to him about Asia during that important meeting his friend said the people in a village asking me to represent them we want your dog to his to stop his head. Why don't you put a belt around the dog's neck this way we would hear your dog coming down the street was a great idea now if I could stay away from the dog it would not be able to buy anyone anymore the dark like the Bell two people look at him when they heard that when when men here to spell the Bell played when he work Monday John Stout stroll through the village and a message on all the dogs expect them to Wong to be a bail like it does a mass at his fail this said the Bell meds people avoid him just shook his head no they look at me because they like the Bell the other dog said you had the wrong idea of what makes you popular of course they like you fell and tells them where you are so they can avoid you you aren't able to find an animal you see being popular isn't something positive when it's for the wrong reason"
truth ="the dogs Bell John's dog was a bad dog he bit people frequently John had great concern about this it was not an appropriate way for a dog to behave his friends in the village always expected that the news about John's dog spread through the village none of the people wanted to go to John's house John trying to instruct the dog to behave but it never worked he tried to be patient and teach the dog to be calm that also didn't work John didn't want to punish the dog how will I stop my dog's John asked himself John's friend came to talk to him about the issue during their important meeting his friend said the people in the village asked me to represent them we want your dog to stop this habit why don't you put a bell around the dog's neck this way we would hear your dog coming down the street John thought this was a great idea stay away from the dog would not be able to buy any more the dog like the people looked at him when they heard his bail this made the dog very content be like the song the Belle Plaine when you want one day John's dog stroll through the village and he expected them to want a bell but they lied to dispel they said the Bell made people avoid him John's dog shook his head no they look at me because they like the Bell the other dogs you have the wrong idea what makes you popular of course they like your bell it tells them where you are so they can you see being popular isn't something positive when it's for the wrong reason"
t = "Well I'm from Brighton England I like to surf and I'm learning to fly small airplanes I don't like to bake cupcakes"
s = "well I'm from flight Angela I like to Surf and I'm learning to fly small airplanes I don't like to bake cupcakes"
print((1-wer(truth, speak)) * 100)
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





