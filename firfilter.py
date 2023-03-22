import numpy as np


class FIRfilter:
    def __init__(self, _coefficients):
        self.ntaps = len(_coefficients)
        self.coefficients = _coefficients
        self.buffer = np.zeros(self.ntaps)

    def dofilter(self, v):
        for j in range(self.ntaps - 1):
            self.buffer[self.ntaps - j - 1] = self.buffer[self.ntaps - j - 2]
        self.buffer[0] = v
        return np.inner(self.buffer, self.coefficients)

    def doFilterAdaptive(self, signal, noise, learningRate=0.1):
        canceller = self.dofilter(noise)
        output_signal = signal - canceller
        for j in range(self.ntaps):
            self.coefficients[j] = self.coefficients[j] + output_signal * learningRate * self.buffer[j]
        return output_signal
