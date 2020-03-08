import pyaudio
import numpy as np
import struct
import matplotlib.pyplot as plt

import wave
import sys
import os
from scipy import fftpack

CHUNK = 1024 * 4 # 4096 samples per chunk
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100 # 44.1KHZ samples per second

np.set_printoptions(threshold=sys.maxsize)

def play_wave(pyaudio_obj):
	# wf = wave.open(sys.argv[1], 'rb') # uncomment if multiple wav files
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

	# play stream
	while len(data) > 0:
		stream.write(data)
		data = wf.readframes(CHUNK)

	# stop stream
	stream.stop_stream()
	stream.close()

	# close PyAudio
	p.terminate()

def visualize_audio_stream(pyaudio_obj):

	stream = pyaudio_obj.open(
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

	line, = wave_ax.plot(x, np.random.rand(CHUNK)) # initialize random arrays to be overwritten in loop
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
		
		# calculate frequency power and parameters
		freq = fftpack.fft(data_int)
		power = np.abs(freq) # freq magnitude

		pos_mask = np.where(freq > 0) # choose only positive frequencies
		freq_pos = x_freq[pos_mask] # unused for now
		peak_freq = freq_pos[power[pos_mask].argmax()] # return the frequency with highest magnitude

		line_freq.set_ydata(power / CHUNK) 

		# draw
		fig.canvas.draw()
		fig.canvas.flush_events()
		plt.show(block=False)

		# power is of size CHUNK, array of magnitudes of all frequencies from 0 to 22khz
		# print(peak_freq)
		determine_clap(110, 3000, data_int)

# determines whether a clap occurred based on magnitude:
# criteria for clap: must exceed magnitude of 110 3000 samples after first.
def determine_clap(magnitude_threshold, clap_length, data_int):
	if (np.size(np.where(data_int > 120)) > 0):
		print(np.where(data_int > 120))


def main():
	p = pyaudio.PyAudio()
	# play_wave(p)
	visualize_audio_stream(p)

if __name__ == '__main__':
	main()
