import argparse
import numpy as np
import sounddevice as sd
import queue
import sys

import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

def find_most_common_frequency(data, sample_rate):
    """
    Find the most common frequency in a signal within the human audible range using the Fast Fourier Transform (FFT).

    Args:
        data (list): A list of data points representing the time-domain signal.
        sample_rate (float): The sample rate in Hz (samples per second).

    Returns:
        float: The most common frequency in the audible range of the signal.
    """
    # Define the human audible frequency range
    min_freq = 20.0
    max_freq = 2000.0

    # Perform the FFT on the data
    fft_result = np.fft.fft(data)

    # Calculate the corresponding frequencies
    freqs = np.fft.fftfreq(len(data), 1 / sample_rate)

    # Calculate the magnitudes of the FFT coefficients
    magnitudes = np.abs(fft_result)

    # Apply bandpass filter to limit frequencies to the human audible range
    indices = np.where((freqs >= min_freq) & (freqs <= max_freq))
    freqs = freqs[indices]
    magnitudes = magnitudes[indices]

    # Find the index of the maximum magnitude
    max_magnitude_idx = np.argmax(magnitudes)

    # Find the corresponding frequency
    most_common_freq = freqs[max_magnitude_idx]

    return most_common_freq

def create_parser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'filename', nargs='?', metavar='FILENAME',
        help='audio file to store recording to')
    parser.add_argument(
        '-d', '--device', type=int,
        help='input device (numeric ID)')
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')
    parser.add_argument(
        '-r', '--samplerate', type=int, default=44100, help='sampling rate')
    parser.add_argument(
        '-c', '--channels', type=int, default=1, help='number of input channels')
    parser.add_argument(
        '-b', '--blocksize', type=int, default=2048, help='width of sample')
    args = parser.parse_args()

    if args.list_devices:
        print(sd.query_devices())
        sys.exit(0)

    return args


def main():

    standard_tuning = {
        'E': 82.41,   # E2
        'A': 110.00,  # A2
        'D': 146.83,  # D3
        'G': 196.00,  # G3
        'B': 246.94,  # B3
        'E2': 329.63  # E4
    }

    q = queue.Queue()
    args = create_parser()

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            print(status, file=sys.stderr)
        # do stuff with chunk
        mc_freq = find_most_common_frequency(indata, args.samplerate)
        q.put(mc_freq)

    with sd.InputStream(samplerate=args.samplerate, device=args.device, channels=args.channels,
                        callback=callback, blocksize=args.blocksize):
        while True:
            print(f"std_tuning: {standard_tuning}, your freq: {q.get()}")

if __name__ == "__main__":
    main()
