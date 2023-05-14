
from digitalthermostat import DigitalThermostat

class BoilerController:
    def __init__(self, pressureSensor=None, temperatureSensor=None, heaterOutput=None):
        self.thermostat = DigitalThermostat(temperatureSensor, heaterOutput)
        self.pressureSensor = pressureSensor

    def setPressureSensor(self, pressureSensor):
        self.pressureSensor = pressureSensor

    def setTemperatureSensor(self, temperatureSensor):
        self.thermostat.setSensor(temperatureSensor)

    def setOutput(self):
        pass

