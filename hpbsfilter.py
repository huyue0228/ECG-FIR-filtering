import matplotlib.pyplot as plt
import numpy as np

import firfilter
import firfilter_design

# set default size of plots
plt.rcParams['figure.figsize'] = (15, 4)

ecg = np.genfromtxt('ecg.dat')
plt.figure()
plt.plot(ecg)
plt.xlabel("time(ms)")
plt.ylabel("Amplitude")
plt.title("Origin ECG Data")
plt.savefig("origin_ECG_data.svg", dpi=600, format="svg", bbox_inches='tight', pad_inches=0.1)

# to find the baseline wander
ft_ecg = np.fft.fft(ecg)
frequency = np.linspace(0, 1000, len(ft_ecg))
plt.figure()
plt.plot(frequency[:100], np.real(ft_ecg[:100]))
plt.xlabel("Frequency(Hz)")
plt.ylabel("Amplitude")
plt.title("Baseline Wander Spectrum")
plt.savefig("baseline_wander_spectrum.svg", dpi=600, format="svg", bbox_inches='tight', pad_inches=0.1)

# the baseline wander can be found out of 1.5Hz

# set sampling rate
fs = 1000
design = firfilter_design.filterDesign(fs)

# highpass filter to remove DC and the baseline wander
h0 = design.highpassDesign(2)
f0 = firfilter.FIRfilter(h0)
y0 = np.empty(len(ecg))
for j in range(len(ecg)):
    value = ecg[j]
    output = f0.dofilter(value)
    y0[j] = output
plt.figure()
plt.plot(y0)
plt.xlim(0, 5000)
plt.xlabel("time(ms)")
plt.ylabel("Amplitude")
plt.title("Data after highpass filter")
plt.savefig("data_after_highpass_filter.svg", dpi=600, format="svg", bbox_inches='tight', pad_inches=0.1)

# bandstop filter to remove 50Hz
h1 = design.bandstopDesign(45, 55)
f1 = firfilter.FIRfilter(h1)
y1 = np.empty(len(ecg))
for j in range(len(ecg)):
    value = y0[j]
    output = f1.dofilter(value)
    y1[j] = output
plt.figure()
plt.plot(y1)
plt.xlim(0, 5000)
plt.xlabel("time(ms)")
plt.ylabel("Amplitude")
plt.title("Data after highpass and bandstop filter")
plt.savefig("data_after_highpass_and_bandstop_filter.svg", dpi=600, format="svg", bbox_inches='tight', pad_inches=0.1)

plt.figure()
plt.plot(y1[1600:2600])
plt.title("A single heartbeat")
plt.savefig("A single heartbeat.svg", dpi=600, format="svg", bbox_inches='tight', pad_inches=0.1)
plt.show()
