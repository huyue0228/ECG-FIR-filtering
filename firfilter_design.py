import numpy as np


class filterDesign:
    def __init__(self, sampling_rate):
        self.fs = sampling_rate

    def highpassDesign(self, cutoff_frequency):
        fs = self.fs
        fc = cutoff_frequency
        M = 1000
        k = int(fc / fs * M)  # normalised frequency
        X = np.ones(M)
        X[:k + 1] = 0
        X[M - k:M] = 0
        x = np.fft.ifft(X)
        x = np.real(x)
        h = np.zeros(M)
        h[0:int(M / 2)] = x[int(M / 2):M]
        h[int(M / 2):M] = x[0:int(M / 2)]
        h = h * np.hamming(M)
        return h

    def bandstopDesign(self, cutoff_frequency1, cutoff_frequency2):
        fs = self.fs
        fc1 = cutoff_frequency1
        fc2 = cutoff_frequency2
        M = 1000
        k1 = int(fc1 / fs * M)
        k2 = int(fc2 / fs * M)  # normalised frequency
        X = np.ones(M)
        X[k1:k2 + 1] = 0
        X[M - k2:M - k1 + 1] = 0
        x = np.fft.ifft(X)
        x = np.real(x)
        h = np.zeros(M)
        h[0:int(M / 2)] = x[int(M / 2):M]
        h[int(M / 2):M] = x[0:int(M / 2)]
        h = h * np.hamming(M)
        return h
