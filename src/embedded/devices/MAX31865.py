### A micropython library for MAX31865 RTD amplifier:
### https://www.analog.com/media/en/technical-documentation/data-sheets/max31865.pdf 

from machine import Pin, SPI
from micropython import const
import time

# Scoped constants
_RTD_RES = 430 # RTD resistance (ohms)

# Register addresses
_REG_CONFIG = const(0x00)
_REG_RTD_MSB = const(0x01)
_REG_RTD_LSB = const(0x02)
_REG_FAULT_HIGH = const(0x03)
_REG_FAULT_LOW = const(0x05)
_REG_FAULT_STATUS = const(0x07)

_DPOS_VBIAS = const(0b10000000) # bias
_DPOS_CONV = const(0b01000000) # auto-convert
_DPOS_SHOT = const(0b00100000) # one shot mode
_DPOS_NWIRE = const(0b00010000) # set # of wires (2/4 or 3 wire)
_DPOS_CLEAR_FAULT = const(0b00000010)
_DPOS_FILT = const(0b00000001) # Set filter rate (50 or 60hz)

class MAX31865:

    def __init__(self, spi: SPI, cs: Pin, ref=430.0, nom=100.0):
        self.spi = spi
        self.cs = cs
        self.cs(1)
        self.ref_resistance = ref
        self.nom_resistance = nom

        self.enable_3wire(True)
        self.enable_auto(True)
        self.enable_bias(False)
        self.enable_50Hz(False)

    def temp(self):
        res = self.resistance()
        return (res / self.nom_resistance - 1) / 0.00385

    def resistance(self):
        adc_code = self.read_u16(_REG_RTD_MSB)
        return adc_code * self.ref_resistance / 2**15

    def enable_auto(self, auto: bool):
        # Set the conversion mode
        # If true, the chip will perform conversions automatically at a 50 or 60 hz rate.
        self.write_config(_DPOS_CONV, auto)

    def enable_bias(self, bias: bool):
        self.write_config(_DPOS_VBIAS, bias)

    def enable_50Hz(self, enable: bool):
        self.write_config(_DPOS_FILT, enable)

    def enable_3wire(self, enable: bool):
        # If true, enable 3 wire sensing, otherwise 2/4 wire shall be used
        self.write_config(_DPOS_NWIRE, enable)

    def enable_1shot(self, enable: bool):
        # If true, set to one-shot mode
        self.write_config(_DPOS_SHOT, enable)

    def clear_fault(self):
        # self.write_config(_DPOS_FAULT_STATUS, True)
        self.write_config(_DPOS_CLEAR_FAULT, True)

    def write_config(self, config, enable: bool):
        c = self.read_u8(_REG_CONFIG)
        if enable:
            new_config = c | config
            self.write_u8(_REG_CONFIG | 0x80, new_config)
        else:
            new_config = c & ~config
            self.write_u8(_REG_CONFIG | 0x80, new_config)
        
    def write_u8(self, address, value):
        self.cs(0)
        self.spi.write(bytes([address, value]))
        self.cs(1)

    def read_u8(self, address):
        self.cs(0)
        self.spi.write(bytes([address]))
        _b = self.spi.read(1)
        self.cs(1)
        return _b[0]

    def read_u16(self, address):
        self.cs(0)
        self.spi.write(bytes([address]))
        _b = self.spi.read(2)
        msb = _b[0]
        lsb = _b[1]
        self.cs(1)
        return (msb << 7) | (lsb >> 1) 


