# -*- coding: UTF-8 -*-
import wave


def get_wav_time(path):

    f = wave.open(path, 'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    time = nframes / (1.0 * framerate)
    f.close()

    return time
