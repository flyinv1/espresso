
class DigitalThermoStat:
    """ Digital thermostat

        All units in °C
    """

    def __init__(self):
        self.temp = 20

        # Target temperature
        self.target = 20

        # Target switching band - symmetric
        self.band = 1

        # Maximumum switching frequency of control input
        self.max_freq = 1

        # Redlines - tuple (min, max)
        self.redlines = (20, 100)

    @property
    def output(self):
        # Output is read-only
        self.output = 0

    def update(self, temp):
        # Input temperature °C

        # Control logic
        output = 0

        if self.temp > self.target + self.band:
            output = 1
        elif self.temp < self.target - self.band:
            output = 0
        else:
            output = self.output

        if self.temp > self.redlines(1):
            # Temperature too high
            output = 0
            # Raise redline high error
        elif self.temp < self.redlines(0):
            # Temperature too low
            output = 0
            # Raise redline low error

        self.output = output


