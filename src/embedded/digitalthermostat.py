
class DigitalThermostat:
    """ Digital thermostat

        All units in °C
    """

    def __init__(self, temperatureSensor, heaterOutput):
        # Target temperature
        self.target = 20

        # Target switching band - symmetric
        self.band = 1

        # Maximumum switching frequency of control input
        self.max_freq = 1

        self.sensor = temperatureSensor
        self.output = heaterOutput

    def setSensor(self, sensor):
        self.sensor = sensor

    def setOutput(self, output):
        self.output = output

    def update(self):
        # Input temperature °C

        # Control logic
        output = 0

        temp = self.sensor.latest()

        if temp > self.target + self.band:
            output = 1
        elif temp < self.target - self.band:
            output = 0
        else:
            output = self.output.latest()

        self.output.write(output)

    def override(self, output):
        self.output.write(output)

