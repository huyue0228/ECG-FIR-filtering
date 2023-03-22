import matplotlib.pyplot as plt
import numpy as np

import firfilter
import firfilter_design

# set default size of plots
plt.rcParams['figure.figsize'] = (15, 4)


def getPeaks(signal):
    # Mark regions of interest
    window = []
    peaklist = []
    listpos = 0  # use a counter to move over the different data columns

    for datapoint in signal:
        Threshold = 0.6 * np.max(signal)  # Get local mean
        if (datapoint < Threshold) and (len(window) < 1):  # If no detectable R-complex activity -> do nothing
            listpos += 1
        elif datapoint >= Threshold:  # If signal comes above local mean, mark ROI
            window.append(datapoint)
            listpos += 1
        else:  # If signal drops below local mean -> determine highest point
            beatposition = listpos - len(window) + window.index(
                max(window))  # Notate the position of the point on the X-axis
            peaklist.append(beatposition)  # Add detected peak to list
            window = []  # Clear
            listpos += 1
    for i in range(len(peaklist) - 1, -1, -1):
        if abs(peaklist[i] - peaklist[i - 1]) < 20:
            if signal[peaklist[i]] > signal[peaklist[i - 1]]:
                del peaklist[i - 1]
            else:
                del peaklist[i]
    return peaklist


def distance(p):
    d = []
    for i in range(1, len(p)):
        d.append(p[i] - p[i - 1])
    return d


def getBpm(d, fs):
    bpm = 60 * fs / d
    return bpm


ecg = np.genfromtxt('ecg.dat')
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

# bandstop filter to remove 50Hz
h1 = design.bandstopDesign(45, 55)
f1 = firfilter.FIRfilter(h1)
y1 = np.empty(len(ecg))
for j in range(len(ecg)):
    value = y0[j]
    output = f1.dofilter(value)
    y1[j] = output

# matched filter
# create out FIR coefficients by time reversing the template
template = y1[1100:1600]
fir_coeff = template[::-1]  # inverse
# plot a real R peak and the template side by side
plt.figure()
plt.plot(template)
plt.plot(fir_coeff)
plt.title("R-Peak Template")
plt.legend(["Template", "Reversed Template"], loc="upper right")
plt.savefig("R-Peak_template.svg", dpi=600, format="svg", bbox_inches='tight', pad_inches=0.1)

# filter the ECG with the time reversed template
f3 = firfilter.FIRfilter(fir_coeff)
y3 = np.empty(len(ecg))
for j in range(len(ecg)):
    value = y1[j]
    output = f3.dofilter(value)
    y3[j] = output
plt.figure()
plt.plot(y3)
plt.xlim(0, 5000)
plt.xlabel("time(ms)")
plt.ylabel("Amplitude")
plt.title("Data after Matched filter")
plt.savefig("Data_after_Matched_filter.svg", dpi=600, format="svg", bbox_inches='tight', pad_inches=0.1)

# square the result to improve signal to noise ratio
plt.figure()
y4 = y3 * y3
plt.plot(y4)
plt.xlim(0, 5000)
plt.xlabel("time(ms)")
plt.ylabel("Amplitude")
plt.title("Squared data after Matched filter")
plt.savefig("Squared_data_after_Matched_filter.svg", dpi=600, format="svg", bbox_inches='tight', pad_inches=0.1)

# BPM part
peaks = getPeaks(y4)  # location of the peaks
ybeat = [y4[x] for x in peaks]  # Get the y-value of all peaks for plotting purposes
plt.figure()
plt.title("Detected R-Peaks")
plt.plot(y4, label='Squared Wave')  # Plot semi-transparent HR
plt.xlim(0, 5000)
plt.scatter(peaks, ybeat, color='red', label='Peak Point')  # Plot detected peaks
plt.legend(loc="upper left")
plt.savefig("Detected_R-Peaks.svg", dpi=600, format="svg", bbox_inches='tight', pad_inches=0.1)

distances = distance(peaks)  # all the distances between peaks

totalTime = 30
time = np.linspace(0, totalTime, len(peaks))
ybpm = [0]  # set the initial value as 0, maybe 60 will be better?
for i in range(len(distances)):
    yi = getBpm(distances[i], fs)
    ybpm.append(yi)  # average bpm in one minute
plt.figure()
plt.xlabel("time(s)")
plt.ylabel("BPM")
plt.title("Real Time BPM")
plt.plot(time, ybpm)
plt.savefig("Real_Time_BPM.svg", dpi=600, format="svg", bbox_inches='tight', pad_inches=0.1)
plt.show()
