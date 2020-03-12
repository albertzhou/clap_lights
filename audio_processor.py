import pyaudio
import numpy as np
import struct
import matplotlib.pyplot as plt

import wave
import sys
import os
from scipy import fftpack

from datetime import datetime

import ethernet
import serial

## Configuration variables - adjust to suit needs
# audio processor configuration
SENSITIVITY = 120 # choose value between 10-124 (124 is most sensitive to clap)

# Pyaudio configuration
CHUNK = 1024 * 10 # 4096 samples per chunk
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100 # 44.1KHZ samples per second

# Ethernet Configuration
TARGET_IP = "192.168.1.177"
TARGET_PORT = 23

# Serial Configuration
MCU_SERIAL_PORT = '/dev/ttyS2'

# Numpy configuration
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

	clap_present = False

	first_clap_time = datetime(1996, 11, 10 , 0, 0)
	first_clap = False
	last_clap_time = datetime(1996, 11, 10, 0, 0)

	# main loop
	while True:		
		# draw waveform
		data_int, power, freq = process_waveform(stream)
		
		peak_freq = determine_peak_freq(stream, x_freq, freq, power)
		
		# draw (uncomment block for visualizer)
		# line.set_ydata(data_int)
		# line_freq.set_ydata(power / CHUNK) 
		# fig.canvas.draw()
		# fig.canvas.flush_events()
		# plt.show(block=False)

		clap_present = determine_clap(SENSITIVITY, 6000, data_int, power, last_clap_time)
		current_time = datetime.now()
		
		if (clap_present and not first_clap):	
			first_clap_time = current_time
			first_clap = True
		elif (clap_present and first_clap):
			toggle_lights()

		time_since_first_clap = (current_time - first_clap_time).total_seconds()

		# reset first clap if no second clap within maximum time frame
		if (time_since_first_clap > 1):
			first_clap = False

# determines whether a clap occurred based on magnitude:
# criteria for clap: must exceed magnitude_threshold, and be still exceed after 3000 but not 8000 samples after (at 44.1khz SR)
def determine_clap(magnitude_threshold, clap_length, data_int, power, last_clap_time):
	current_time = datetime.now()
	time_since_clap = (current_time - last_clap_time).total_seconds()

	if (time_since_clap < 0.25):
		return False

	if (np.size(np.where(data_int > magnitude_threshold)) > 0):
		loud_locations = np.where(data_int > 120)

		initial_sound = loud_locations[0][0]
		last_sound = loud_locations[0][-1]
		sound_duration = last_sound - initial_sound

		if (sound_duration > clap_length):
			clap_present = True
			# ethernet.send_message(TARGET_IP, TARGET_PORT, "Clap Detected")
			print("detected a clap")
		else:
			clap_present = False
	else:
		clap_present = False

	return clap_present

def process_waveform(stream):
	data = stream.read(CHUNK)
	data_int = np.array(struct.unpack(str(2 * CHUNK) + 'B', data), dtype='b')[::2]
	
	# calculate frequency power and parameters
	freq = fftpack.fft(data_int)
	power = np.abs(freq) # power is of size CHUNK, array of magnitudes of all frequencies from 0 to 22khz

	return [data_int, power, freq]

def determine_peak_freq(stream, x_freq, freq, power):
	pos_mask = np.where(freq > 0) # choose only positive frequencies
	freq_pos = x_freq[pos_mask] # unused for now
	peak_freq = freq_pos[power[pos_mask].argmax()] # return the frequency with highest magnitude

	return peak_freq

# toggle lights by sending message to arduino over serial
def toggle_lights():
		print("toggling lights")
		# ser = serial.Serial(MCU_SERIAL_PORT, 9600, timeout=1)
		# MCU_SERIAL_PORT.write("toggle light")

def main():
	p = pyaudio.PyAudio()
	# play_wave(p)
	visualize_audio_stream(p)

if __name__ == '__main__':
	main()
