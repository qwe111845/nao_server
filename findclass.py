# -*- coding: UTF-8 -*-



#transcribe_gcs("gs://speech_to_text_class/d0342273 2019-03-07 17'58-record wav")

from jiwer import wer


d = dict(icc=['aa', 'bb'], qq=[1, 3])
d['icc'].append('11')
print(d)
speak = "the laboratory Mia's father had a laboratory but she had no idea what was in it her dad always closed " \
     "and locked the door when she knew that he used it to do projects for work he never told me what these " \
     "projects were one night Mia approach the door to the laboratory she stopped and thought I wonder what " \
     "crazy experiment he is doing now she heard a loud noise it sounded like an evil laugh the noise scared " \
     "her so she walked quickly back to her room the next night her friend Liz came to her house when Liz arrived" \
     " Mia told her about the night before it was terrible she said Adventure nervous about going into " \
     "her father's laboratory but she agreed as always the door was locked they waited until me is father " \
     "he didn't lock the door said let's go the laboratory was dark the girls walk down the stairs " \
     "carefully Mia smells strange chemicals what terrible thing was walking suddenly they heard an evil " \
     "laugh it was even worse than the one me I heard the night before what if a monster was going to kill " \
     "them me I had to do something she shouted for help me as father ran into the room and turned on the lights " \
     "he said you must have learned my secret monster tried to kill us me a sad monster the doll that didn't " \
     "sound so evil anymore I made this for your birthday I wanted to give it to you then but you can " \
    "have it now I hope you like it"

truth = "The Laboratory Mia's father had a laboratory but she had no idea what was in it Her dad always closed " \
     "and locked the door when he went in She knew that he used it to do projects for work He never told Mia " \
     "what these projects were One night Mia approached the door to the laboratory She stopped and thought I " \
     "wonder what crazy experiment he is doing now Suddenly she heard a loud noise It sounded like an evil " \
     "laugh The noise scared her so she walked quickly back to her room The next night her friend Liz came " \
     "to her house When Liz arrived Mia told her about the night before Oh it was terrible she said Why " \
     "don't we see what is in there Liz asked It will be a fun adventure  Mia felt nervous about going into" \
     " her father's laboratory but she agreed As always the door was locked They waited until Mia's father " \
     "left the laboratory to eat dinner He didn't lock the door Liz said Let's go The laboratory was dark " \
     " The girls walked down the stairs carefully Mia smelled strange chemicals What terrible thing was her" \
     " father creating Suddenly they heard an evil laugh It was even worse than the one Mia heard the night" \
     " before What if a monster was going to kill them Mia had to do something She shouted for help Mia's" \
     " father ran into the room and turned on the lights Oh no he said You must have learned my secret Your " \
     "monster tried to kill us Mia said Monster he asked You mean this He had a pretty doll in his hands " \
     "The doll laughed The laugh didn't sound so evil any more I made this for your birthday I wanted to " \
     "give it to you then but you it now I hope you like it"

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





