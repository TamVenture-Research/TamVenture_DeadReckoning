import numpy as np

GRAVITY = 9.81


class AdaptiveJerkPaceThreshold:
    def __init__(self, zero = GRAVITY):
        self.zero = zero
        self.last_state = None
        self.last_trough = None
        self.last_peak = None
        self.peak_troughs = [] # accepted troughs
        self.meta = []
        self.jerk_mean = 1
        self.alpha = 0.125
        self.jerk_dev = 0.125
        self.beta = 0.25
    def detect(self, timestamp, datum):
        accept = False
        current_state = None
        if datum < self.zero:
            current_state = 'trough'
            if self.last_trough is None or datum < self.last_trough["val"]:
                self.last_trough = {"val": datum, "ts": timestamp, "min_max": "min"}
        elif datum >= self.zero:
            current_state = 'peak'
            if self.last_peak is None or datum > self.last_peak["val"]:
                self.last_peak = {"val": datum, "ts": timestamp, "min_max": "max"}

        # a crossing has been detected!!
        if current_state != self.last_state:
            # if we go from trough to peak
            if self.last_state == 'trough':
                if self.last_peak:
                    jerk = self.last_peak['val'] - self.last_trough['val'] # look at the difference

                    # if the difference is large enough then record the trough
                    if jerk > self.jerk_mean - 4 * self.jerk_dev:
                        self.jerk_mean = jerk * self.alpha + self.jerk_mean * (1- self.alpha)
                        self.jerk_dev = abs(jerk) * self.beta + jerk * (1 - self.beta)

                        self.meta.append([timestamp, self.jerk_mean, self.jerk_dev])
                        self.peak_troughs.append(self.last_trough)
                        self.last_trough = None
                        accept = True
            # if we go from peak to trough
            elif self.last_state == 'peak':
                self.last_peak = None
        self.last_state = current_state

        return accept
def adaptive_step_jerk_threshold(data, timestamps, zero=GRAVITY):
    asjt = AdaptiveJerkPaceThreshold(zero)
    for timestamp, datum in zip(timestamps, data):
        accept = asjt.detect(timestamp, datum)

    return np.array(asjt.peak_troughs), asjt.meta