import pyaudio
import numpy as np
import struct
import matplotlib.pyplot as plt

import wave
import sys
import os
from scipy import fftpack

CHUNK = 1024 * 6 # 4096 samples per chunk
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100 # 44.1KHZ samples per second

def play_wave():
	# wf = wave.open(sys.argv[1], 'rb')
	wf = wave.open("CantinaBand3.wav", 'rb')

	# get information about wav file
	num_samples = wf.getnframes()
	print("Num Samples: " + str(num_samples))
	sample_rate = wf.getframerate()
	print("Sample Rate: " + str(sample_rate) + " Hz")
	duration = round(num_samples / sample_rate, 4)
	print("Duration: " + str(duration))

	# instantiate PyAudio (1)
	p = pyaudio.PyAudio()

	# open stream (2)
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
	                channels=wf.getnchannels(),
	                rate=wf.getframerate(),
	                output=True)

	# read data
	data = wf.readframes(CHUNK)

	# play stream (3)
	while len(data) > 0:
	    stream.write(data)
	    data = wf.readframes(CHUNK)

	# stop stream (4)
	stream.stop_stream()
	stream.close()

	# close PyAudio (5)
	p.terminate()

def main():
	p = pyaudio.PyAudio()

	stream = p.open(
		format=FORMAT,
		channels=CHANNELS,
		rate=RATE,
		input=True,
		output=False,
		frames_per_buffer=CHUNK
		)

	fig, (wave_ax, freq_ax) = plt.subplots(2, figsize=(10, 9))

	# plotting variables
	x = np.arange(0, 2 * CHUNK, 2)
	x_freq = np.linspace(0, RATE, CHUNK) # array from 0 to 44.1khz in increments of (6*1024)

	line, = wave_ax.plot(x, np.random.rand(CHUNK)) # initialize random array to be overwritten
	line_freq, = freq_ax.plot(x_freq, np.random.rand(CHUNK))

	wave_ax.set_ylim(-150, 150)
	wave_ax.set_xlim(0, CHUNK)
	wave_ax.set_title("Wave visualizer")
	wave_ax.set_xlabel("Samples")
	wave_ax.set_ylabel("Volume")

	freq_ax.set_title("Frequency Spectrum")
	freq_ax.set_xlabel("Frequency (Hz)")
	freq_ax.set_ylabel("Frequency Magnitude")
	freq_ax.set_xlim(0, RATE / 2) # crop out negative frequencies and anything above nyquist freq

	while True:
		data = stream.read(CHUNK)
		
		# draw waveform
		data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2]
		line.set_ydata(data_int)
		
		# draw frequency spectrum
		x_freq = fftpack.fft(data_int)
		line_freq.set_ydata(np.abs(x_freq) / CHUNK)

		fig.canvas.draw()
		fig.canvas.flush_events()
		plt.show(block=False)

		# print(data_int)

if __name__ == '__main__':
	# play_wave()
	main()
