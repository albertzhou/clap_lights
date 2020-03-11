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

def main():
	datetime_test()

if __name__ == '__main__':
	main()
