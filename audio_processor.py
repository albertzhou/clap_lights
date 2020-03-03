import pyaudio
import numpy as np
import struct
import matplotlib.pyplot as plt

import wave
import sys
import os

def play_wave():
	CHUNK = 1024

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
	CHUNK = 1024 * 4 # 4096 samples per chunk
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100 # 44.1KHZ samples per second

	p = pyaudio.PyAudio()

	stream = p.open(
		format=FORMAT,
		channels=CHANNELS,
		rate=RATE,
		input=True,
		output=False,
		frames_per_buffer=CHUNK
		)

	plt.show(block=False)

	fig, ax = plt.subplots()

	x = np.arange(0, 2 * CHUNK, 2)
	line, = ax.plot(x, np.random.rand(CHUNK))
	ax.set_ylim(0, 255)
	ax.set_xlim(0, CHUNK)

	while True:
		data = stream.read(CHUNK)
		data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2] + 127
		line.set_ydata(data_int)
		fig.canvas.draw()
		fig.canvas.flush_events()

		print(data_int)

if __name__ == '__main__':
	play_wave()
	main()
