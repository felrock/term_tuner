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

def callback(in_data, frame_count, time_info, status):
    """ callback for playback data """
    np_data = np.fromstring(in_data, dtype=np.int16)

    # get frequency buckets
    p_decibel = 20*np.log10(np.abs(np.fft.rfft(np_data)))
    freq = np.linspace(0, RATE/2.0, len(p_decibel))
    pair_pf = zip(p_decibel, freq)
    
    # find the fq with the highest power
    amp = -1
    fq = 0
    for ppf in pair_pf:
        if ppf[0] > amp:
            amp = ppf[0]
            fq = ppf[1]
    
    # see which string the highst fq matches
    string = ""
    delta_freq = len(p_decibel)
    for gs, gfq in GUITAR_STRING_FREQS.items():
        dfq = abs(gfq - fq)
        if abs(gfq - fq) < delta_freq:
            delta_freq = dfq
            string = gs
    print("String: ", string)

    # If len(data) is less than requested frame_count, PyAudio automatically
    # assumes the stream is finished, and the stream stops.
    return (in_data, pyaudio.paContinue)

def main():
    # Instantiate PyAudio and initialize PortAudio system resources (2)
    p = pyaudio.PyAudio()

    # Open stream using callback (3)
    stream = p.open(format=pyaudio.paInt16,
                    channels=CHANNEL,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback=callback)

    # Wait for stream to finish (4)
    while stream.is_active():
        time.sleep(0.1)

    # Close the stream (5)
    stream.close()

    # Release PortAudio system resources (6)
    p.terminate()

if __name__ == "__main__":
    main()
