
from tkinter import W
from .virtualsignal import VirtualSignal

class VirtualIOControllerDisplayState:
    STANDBY="STANDBY"
    PREHEATING="PREHEATING"
    DISPENSING="DISPENSING"
    STEAMING="STEAMING"

class VirtualIOController:

    def __init__(self, panel):

        self.panel = panel
        
        self.boilerPressureSignal = VirtualSignal()
        self.boilerTemperatureSignal = VirtualSignal()
        self.bypassTemperatureSignal = VirtualSignal()
        self.groupheadPressureSignal = VirtualSignal()
        self.groupheadTemperatureSignal = VirtualSignal()
        self.boilerTemperatureCommandSignal = VirtualSignal()
        self.boilerPressureCommandSignal = VirtualSignal()
        self.groupheadTemperatureCommandSignal = VirtualSignal()
        self.groupheadPressureCommandSignal = VirtualSignal()
        self.machineEnableCommandSignal = VirtualSignal()
        self.boilerEnableCommandSignal = VirtualSignal()
        self.shotEnableCommandSignal = VirtualSignal()

        self.boilerValveSignalOutput = VirtualSignal()
        self.groupheadValveSignalOutput = VirtualSignal()
        self.bypassValveSignalOutput = VirtualSignal()
        self.drainValveSignalOutput = VirtualSignal()
        self.pumpRPMSignalOutput = VirtualSignal()
        self.groupheadHeaterASignalOutput = VirtualSignal()
        self.groupheadHeaterBSignalOutput = VirtualSignal()
        self.boilerHeaterSignalOutput = VirtualSignal()

        self.signals = [
            self.boilerPressureSignal,
            self.boilerTemperatureSignal,
            self.groupheadPressureSignal,
            self.groupheadTemperatureSignal,
            self.boilerTemperatureCommandSignal,
            self.boilerPressureCommandSignal,
            self.groupheadTemperatureCommandSignal,
            self.groupheadPressureCommandSignal,
            self.machineEnableCommandSignal,
            self.boilerEnableCommandSignal,
            self.shotEnableCommandSignal
        ]

        self.outputs = [
            self.boilerValveSignalOutput,
            self.groupheadValveSignalOutput,
            self.bypassValveSignalOutput,
            self.drainValveSignalOutput,
            self.pumpRPMSignalOutput,
            self.groupheadHeaterASignalOutput,
            self.groupheadHeaterBSignalOutput,
            self.boilerHeaterSignalOutput
        ]

        # Connect UI events to iocontroller signals
        self.panel.connect(self)

    def writeDisplay(self):
        self.panel.display.setText("{}\
                \nBoiler:\t\t{:0.1f}/{:0.1f} psig\
                \n\t\t{:0.1f}/{:0.1f} °C\
                \nBypass:\t{:0.1f} °C\
                \nGrouphead:\t{:0.1f}/{:0.1f} psig\
                \n\t\t{:0.1f}/{:0.1f} °C\
                ".format(
                VirtualIOControllerDisplayState.STANDBY,
                self.boilerPressureSignal.current,
                self.boilerPressureCommandSignal.current,
                self.boilerTemperatureSignal.current,
                self.boilerTemperatureCommandSignal.current,
                self.bypassTemperatureSignal.current,
                self.groupheadPressureSignal.current,
                self.groupheadPressureCommandSignal.current,
                self.groupheadTemperatureSignal.current,
                self.groupheadTemperatureCommandSignal.current
            ))

    def setRGB(self, color: str):
        pass
    
    def clearRGB(self):
        pass

    def update(self):
        self.writeDisplay()
