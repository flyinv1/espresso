import utils

class Output:

    def __init__(
            self, 
            units=None, 
            signal=None, 
            logical=False,
            maxFrequency=200, 
            limits=None
    ):
        self.units = units
        self.signalOutput = signal
        self.logical = logical
        self.maxFrequency = maxFrequency
        self.limits = limits

    def write(self, value):
        # Write a floating point value to the signal output
        self.signalOutput.write(utils.clamp(value, self.limits[0], self.limits[1]))

    def sample(self):
        # Return the latest value written to the signal output
        return self.signalOutput.latest()
