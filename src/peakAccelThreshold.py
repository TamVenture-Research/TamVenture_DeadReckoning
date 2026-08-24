"""
Computing number of steps using threshold for detecting peaks
unsatisfactory approach: static threshold is not a reliable method for counting steps of individuals with different walking styles
"""

import numpy as np

class PeakAccelerationThreshold:
    def __init__(self, threshold):
        self.last_state = None
        self.crest_troughs = 0
        self.crossings = []
        self.threshold = threshold

    def detect(self, timestamp, datum):
        current_state = self.last_state
        if datum < self.threshold:
            current_state = 'below'
        elif datum > self.threshold:
            current_state = 'above'
        if current_state is not self.last_state:
            self.crossings.append([timestamp, current_state])
            self.crest_troughs += 1
            self.last_state = current_state
            return True

        self.last_state = current_state
        return False


def peak_accel_threshold(data, timestamps, threshold):
    pat = PeakAccelerationThreshold(threshold)

    for timestamp, datum in zip(timestamps, data):

        crossed = pat.detect(timestamp, datum)

    return np.array(pat.crossings)