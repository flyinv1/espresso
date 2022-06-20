
from boilercontroller import BoilerController
from sensor import Sensor
from output import Output
from flag import FlagManager
import os
import utils
import time

class EspressoManager:
    def __init__(self, iocontroller):
        self.flagManager = FlagManager()
        self.io = iocontroller
        self.initSensors()
        self.initOutputs()
        self.boiler = BoilerController(
            self.boilerPressure,
            self.boilerTemperature,
            self.boilerHeater)

    def initSensors(self):
        # Initialize each sensor
        #   - Use hardware decoupled signals to pipe in sensor data
        #   - IOController members can pass 'real' data or virtualized signals
        #     from simulated fluid and input systems
        
        self.boilerPressure = Sensor(
            "BOILER_PRESS",
            units="psi",
            signal=self.io.boilerPressureSignal)

        self.boilerTemperature = Sensor(
            "BOILER_TEMP",
            units="degC",
            signal=self.io.boilerTemperatureSignal)

        self.bypassTemperature = Sensor(
            "BYPASS_TEMP",
            units="degC",
            signal=self.io.bypassTemperatureSignal
        )

        self.groupheadPressure = Sensor(
            "GROUPHEAD_PRESS",
            units="psi",
            signal=self.io.groupheadPressureSignal)

        self.groupheadTemperature = Sensor(
            "GROUPHEAD_TEMP",
            units="degC",
            signal=self.io.groupheadTemperatureSignal)

        # Command sensors store _instantaneous_ commanded pressure and temperature
        self.boilerPressureCommand = Sensor(
            "C_BOILER_PRESS",
            units="psi",
            signal=self.io.boilerPressureCommandSignal)

        self.boilerTemperatureCommand = Sensor(
            "C_BOILER_TEMP",
            units="degC",
            signal=self.io.boilerTemperatureCommandSignal)

        self.groupheadPressureCommand = Sensor(
            "C_GROUPHEAD_PRESS",
            units="psi",
            signal=self.io.groupheadPressureCommandSignal)

        self.groupheadTemperatureCommand = Sensor(
            "C_GROUPHEAD_TEMP",
            units="degC",
            signal=self.io.groupheadTemperatureCommandSignal)

        self.machineEnableCommand = Sensor(
            "C_MACHINE_EN",
            units=None,
            signal=self.io.machineEnableCommandSignal)

        self.boilerEnableCommand = Sensor(
            "C_BOILER_EN",
            units=None,
            signal=self.io.boilerEnableCommandSignal)

        self.sensors = [
            self.boilerPressure,
            self.boilerTemperature,
            self.bypassTemperature,
            self.groupheadPressure,
            self.groupheadTemperature,
            self.boilerPressureCommand,
            self.boilerTemperatureCommand,
            self.groupheadPressureCommand,
            self.groupheadTemperatureCommand,
            self.machineEnableCommand,
            self.boilerEnableCommand
        ]

    def initOutputs(self):
        self.boilerValve = Output(
            "BOILER_VALVE",
            signal=self.io.boilerValveSignalOutput)

        self.groupheadValve = Output(
            "GROUPHEAD_VALVE",
            signal=self.io.groupheadValveSignalOutput)

        self.bypassValve = Output(
            "BYPASS_VALVE",
            signal=self.io.bypassValveSignalOutput)

        self.drainValve = Output(
            "DRAIN_VALVE",
            signal=self.io.drainValveSignalOutput)

        self.pumpRPM = Output(
            "PUMP_RPM",
            signal=self.io.pumpRPMSignalOutput)

        self.groupheadHeaterA = Output(
            "GROUPHEAD_HEATER_A",
            signal=self.io.groupheadHeaterASignalOutput)

        self.groupheadHeaterB = Output(
            "GROUPHEAD_HEATER_B",
            signal=self.io.groupheadHeaterBSignalOutput)

        self.boilerHeater = Output(
            "BOILER_HEATER",
            signal=self.io.boilerHeaterSignalOutput)

        self.outputs = [
            self.boilerValve,
            self.groupheadValve,
            self.bypassValve,
            self.drainValve,
            self.pumpRPM,
            self.groupheadHeaterA,
            self.groupheadHeaterB,
            self.boilerHeater
        ]

    def update(self):
        self.io.update()

