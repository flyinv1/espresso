

class Sensor:
    def __init__(
            self,
            id_str,
            signal=None, 
            sampleFrequency=10, 
            units=None, 
            bufferSize=100,
            transform=None,
            flagManager=None,
            redlines=None
    ):
        # String describing units
        self.units = units

        # Signal to sample data
        self.signal = signal

        # SISO transform function applied to raw data
        self.transform = transform

        # Buffer for transformed data
        self.dataBuffer = []

        # Buffer for raw data
        self.rawBuffer = []

        # Sample frequency [Hz]
        self.sampleFrequency = sampleFrequency

        # DI flag manager where flags are passed
        self.flagManager = flagManager

        # Sensor redlines to detect out of bounds conditions
        self.redlines = redlines

    def setUnits(self, units):
        self.units = units

    def setTransform(self, transform):
        self.transform = transform

    def setSampleFrequency(self, frequency):
        self.frequency = frequency

    def setSampleBufferSize(self, bufferSize):
        self.dataBuffer = []
        self.rawBuffer = []

    def setSignal(self, signal):
        self.signal = signal

    def read(self, indices=None):
        # Return the latest transformed value
        if indices is None:
            return self.dataBuffer[0]
        else:
            return self.dataBuffer[indices[0]:indices[1]]

    def update(self):
        # Sample signal for raw, untransformed data
        #   Note that this is not necessarily the raw ADC value, but
        #   may be modified by an external chip, as in the case of RTD data
        raw = self.signal.value()

        # Apply transform to the data
        data = raw if self.transform is None else self.transform(raw)

        # Update data buffers
        self.rawBuffer.append(raw)
        self.dataBuffer.append(data)

        # Update flags if transformed data exceed redline bounds
        if data < self.redlines[0]:
            self.flagManager.redlineLow(
                self.id_str,
                self.redlines,
                data
            )
        if data > self.redlines[1]: 
            self.flagManager.redlineHigh(
                self.id_str,
                self.redlines,
                data
            )

    def value(self):
        # Duck the signal and return the latest buffer value
        return self.dataBuffer[0]
