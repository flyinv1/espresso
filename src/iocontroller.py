
from micropython import const

_MUX_S0 = 23
_MUX_S1 = 23
_MUX_S2 = 23
_MUX_A0 = 23
_SPI_DT = 23
_SPI_CL = 23
_SPI_CS_BOILER_RTD = 23
_SPI_CS_GROUP_RTD = 23
_SPI_CS_BYPASS_RTD = 23
_MUX_INDEX_BOILER_PRESSURE = 0
_MUX_INDEX_GROUP_PRESSURE = 1
_MUX_INDEX_BOILER_TEMP_COMMAND = 2
_MUX_INDEX_BOILER_PRESSURE_COMMAND = 3
_MUX_INDEX_GROUP_TEMP_COMMAND = 4
_MUX_INDEX_GROUP_PRESSURE_COMMAND = 5
_MUX_INDEX_MACHINE_ENABLE_COMMAND = 6
_MUX_INDEX_BOILER_ENABLE_COMMAND = 7

class IOController:
    def __init__(self):
        
        # Initialize display
        # Initialize RGBLED
        # x Initialize multiplexer
        # Initialize SPI

        self.mux = multiplexerCD74()
        self.boilerPressureSignal = MUXSignal(self.mux)
        self.boilerTemperatureSignal = RTDSignal(self.spi)
        self.groupheadPressureSignal = MUXSignal(self.mux)
        self.groupheadTemperatureSignal = RTDSignal(self.spi)
        self.boilerTemperatureCommandSignal = MUXSignal(self.mux)
        self.boilerPressureCommandSignal = MUXSignal(self.mux)
        self.groupheadTemperatureCommandSignal = MUXSignal(self.mux)
        self.groupheadPressureCommandSignal = MUXSignal(self.mux)
        self.machineEnableCommandSignal = AnalogSignal()
        self.boilerEnableCommandSignal = AnalogSignal()
        self.shotEnableCommandSignal = Signal()

        self.boilerValveSignalOutput = SignalOutput()
        self.groupheadValveSignalOutput = SignalOutput()
        self.bypassValveSignalOutput = SignalOutput()
        self.drainValveSignalOutput = SignalOutput()
        self.pumpRPMSignalOutput = SignalOutput()
        self.groupheadHeaterASignalOutput = SignalOutput()
        self.groupheadHeaterBSignalOutput = SignalOutput()
        self.boilerHeaterSignalOutput = SignalOutput()

    def writeDisplay(self, str: str):
        pass

    def clearDisplay(self):
        pass

    def setRGBState(self, rgbState):
        pass

    def clearRGB(self):
        pass

    def signals(self):
        pass

    def outputs(self):
        pass



