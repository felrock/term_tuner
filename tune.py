import audioop
import numpy as np
import pyaudio
import time
import wave

RATE = 44100
CHANNEL = 2
CHUNK = 2048
GUITAR_STRING_FREQS = {
    "E_1": 82,
    "B_2": 110,
    "G_3": 146,
    "D_4": 196,
    "A_5": 247,
    "E_6": 330,
}

def getXMostCommonFreqencies(data, x, frame_rate):

    w = np.fft.fft(x)
    freq = np.fft.fftfreq(len(w))
    freq_as_hz
    pass


if __name__ == "__main__":
    pass
