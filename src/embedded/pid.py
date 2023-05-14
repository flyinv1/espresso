
class PID():

    def __init__(self, p_gain, i_gain, d_gain, windup_threshold=None):
        self.output = 0 
        self._p_gain = p_gain
        self._i_gain = i_gain
        self._d_gain = d_gain
        self._p = 0
        self._i = 0
        self._d = 0
        self._target = 0
        self._prev = 0
        self._windup = windup_threshold

    def set_target(self, target):
        self._target = target

    def set_windup(self, windup_threshold):
        self._windup = windup_threshold

    def set_gains(self, p_gain, i_gain, d_gain):
        self._p_gain = p_gain
        self._i_gain = i_gain
        self._d_gain = d_gain

    def update(self, value, dt):
        if self._windup is None:
            self._i = self._i + value * dt
        else:
            if self.output < self._windup:
                self._i = self._i + value * dt
        self._d = (value - self._prev) / dt
        self._p = self.target - value
        self.output = (
            self._p * self._p_gain + 
            self._i * self._i_gain + 
            self._d * self._d_gain
        )
