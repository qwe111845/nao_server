

def upload_and_record(db, sid, path):
    import WavInfo
    import cloud_speech
    from jiwer import wer
    print('begin to get reading')

    unit, reading_len, content = db.get_reading_content(sid)
    print('finish get reading')

    print('begin to upload google cloud')
    destination_blob_name = 'unit ' + str(unit) + '/' + sid + '.wav'
    cloud_speech.upload_blob("speech_to_text_class", path, destination_blob_name)
    print('begin to transcribe file')
    gcs_url = "gs://speech_to_text_class/" + destination_blob_name
    transcript, confidence = cloud_speech.transcribe_gcs(gcs_url)
    print('finis transcribe')

    print('Start calculating reading speed and word error rate')
    reading_time = WavInfo.get_wav_time(path)
    reading_speed = int(reading_len / (reading_time / 60.0))
    word_error_rate = (1 - wer(content.encode('utf-8'), str(transcript))) * 100
    word_error_rate = float('%.4f' % word_error_rate)

    db.record_reading(sid, unit, transcript, reading_speed, word_error_rate, confidence)




