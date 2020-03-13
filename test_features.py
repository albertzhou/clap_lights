import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack

import datetime
import time

def fft_test():
	f = 10 # frequency
	f_s = 100 # sampling rate

	t = np.linspace(0, 2, 2*f_s, endpoint=False) # create time values for raw data
	x = np.sin(f * 2 * np.pi * t)

	x_freq = fftpack.fft(x)
	freqs = fftpack.fftfreq(len(x)) * f_s

	print(x_freq) # y axis (but only positive part)
	print(freqs) # x axis

	fig, ax = plt.subplots()

	ax.stem(freqs, np.abs(x_freq))
	ax.set_xlim(0, f_s / 2)
	ax.set_xlabel('Frequency (Hz)')
	ax.set_ylabel('Frequency Amplitude')

	plt.show()

def numpy_where_test():
	a = np.arange(10)
	print(np.where(a < 4))

def datetime_test():
	time_1 = datetime.datetime.now()
	time.sleep(3)
	time_2 = datetime.datetime.now()

	delta_time = time_2 - time_1

	delta_time_s = delta_time.total_seconds()

	print(time_1)
	print(time_2)
	print(delta_time_s)

def set_y_data():
	x = np.arange(-3, 3, .1)
	y = np.sin( np.pi*x)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	#plot a line along points x,y
	line, = ax.plot(x, y)
	#update data
	j = 2
	y2 = np.sin( np.pi*x*j ) / ( np.pi*x*j )
	#update the line with the new data
	line.set_ydata(y2)

	print(x)
	print(y2)

	plt.show()

def hp_filter():
	import numpy as np
	from scipy.fftpack import rfft, irfft, fftfreq

	time   = np.linspace(0,10,2000)
	signal = np.cos(5*np.pi*time) + np.cos(7*np.pi*time)

	W = fftfreq(signal.size, d=time[1]-time[0])
	f_signal = rfft(signal)

	# If our original signal time was in seconds, this is now in Hz    
	cut_f_signal = f_signal.copy()
	cut_f_signal[(W<6)] = 0

	cut_signal = irfft(cut_f_signal)

	import pylab as plt
	plt.subplot(221)
	plt.plot(time,signal)
	plt.subplot(222)
	plt.plot(W,f_signal)
	plt.xlim(0,10)
	plt.subplot(223)
	plt.plot(W,cut_f_signal)
	plt.xlim(0,10)
	plt.subplot(224)
	plt.plot(time,cut_signal)
	plt.show()

def serial_read():

	import serial
	import sys
	import time

	port = "/dev/ttyACM0"

	baudrate = 9600

	ser = serial.Serial(port, baudrate)

	while 1:
	    print(ser.readline().decode('utf-8'))
	    sys.stdout.flush()

def main():
	serial_read()

if __name__ == '__main__':
	main()
