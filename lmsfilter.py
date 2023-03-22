import matplotlib.pyplot as plt
import numpy as np

import firfilter

plt.rcParams['figure.figsize'] = (15, 4)

ecg = np.genfromtxt('ecg.dat')

fs = 1000
M = 1000
noise = 50
learningRate = 0.001

f2 = firfilter.FIRfilter(np.zeros(M))
y2 = np.empty(len(ecg))
for j in range(len(ecg)):
    ref_noise = np.sin(2.0 * np.pi * noise / fs * j)
    y2[j] = f2.doFilterAdaptive(ecg[j], ref_noise, learningRate)
plt.figure()
plt.plot(y2)
plt.xlim(0, 5000)
plt.xlabel("time(ms)")
plt.ylabel("Amplitude")
plt.title("Data after LMS filter")
plt.savefig("data_after_LMS_filter.svg", dpi=600, format="svg", bbox_inches='tight', pad_inches=0.1)
plt.show()
