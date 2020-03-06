import matplotlib.pyplot as plt
import numpy as np
from scipy import fftpack

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
