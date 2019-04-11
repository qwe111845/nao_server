# -*- coding: UTF-8 -*-

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
        audio_channel_count=2,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

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


# transcript, avg_confidence = transcribe_gcs('gs://speech_to_text_class/unit 10/unit10.wav')



def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


upload_blob("speech_to_text_class", r"C:\Users\lin\PycharmProjects\nao_server\record\m0626957\m0626957 2019-04-10 2"
                                    r"0'10-record.wav", "unit 10/m0626957.wav")
