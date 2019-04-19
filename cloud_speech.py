# -*- coding: utf-8 -*-
import os
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/lin/Desktop/googlecloud/Speech To Text class-225971fffeaf.json"


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        audio_channel_count=4,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=120)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    transcript = ''
    avg_confidence = 0.0
    confidence = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        transcript += result.alternatives[0].transcript
        avg_confidence += result.alternatives[0].confidence
        confidence.append(result.alternatives[0].confidence)
        # print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        # print('Confidence: {}'.format(result.alternatives[0].confidence))

    avg_confidence = avg_confidence / len(confidence)

    print(transcript)
    print(confidence)
    print(avg_confidence)

    return transcript, float('%.4f' % avg_confidence)


"""
import WavInfo
from jiwer import wer
import database as d
db = d.MysqlClass()
sid = "d0441423"
unit, reading_len, content = db.get_reading_content(sid)
path = "record/d0441423/d0441423 2019-04-16 19'52-record.wav"
transcript, confidence = transcribe_gcs("gs://speech_to_text_class/unit 5/d0441423.wav")
reading_time = WavInfo.get_wav_time(path)
reading_speed = int(reading_len / (reading_time / 60.0))
print (type(transcript))
print (type(content))
print reading_speed
word_error_rate = (1 - wer(content.encode('utf-8'), str(transcript))) * 100
word_error_rate = float('%.4f' % word_error_rate)

db.record_reading(sid, unit, transcript, reading_speed, word_error_rate, confidence)
"""

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))



