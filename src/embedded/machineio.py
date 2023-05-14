from machine import (Pin, SPI, ADC, SoftSPI)

from devices.RGBLED import RGBLED as rgb
from devices.MAX31865 import MAX31865
from devices.multiplexerCD74 import MultiplexerCD74 as MUX

LED_PIN = 25
SV_GROUP_PIN = 9
SV_FILL_PIN = 13
SV_STEAM_PIN = 12
H_BOILER_PIN = 11
H_GROUP_PIN = 10
PUMP_PIN = 28

class MachineIO:

    def __init__(self, spi=None):

        # Built-in status LED
        self._onboard_led = Pin(LED_PIN, Pin.OUT, value=1)       # Default to this LED being on when the board is powered

        # Devices
        self._sv_group = Pin(SV_GROUP_PIN, Pin.OUT, value=0)     # Grouphead run valve
        self._sv_fill = Pin(SV_FILL_PIN, Pin.OUT, value=0)       # Boiler fill valve
        self._sv_steam = Pin(SV_STEAM_PIN, Pin.OUT, value=0)     # Boiler steam valve
        self._h_boiler = Pin(H_BOILER_PIN, Pin.OUT, value=0)     # Boiler heater
        self._h_group = Pin(H_GROUP_PIN, Pin.OUT, value=0)       # Group heater
        self._pump = Pin(PUMP_PIN, Pin.OUT, value=0)             # Pump run pin
        
        # Primary LED
        self._rgb = rgb(17, 15, 14)
        
        # Run button
        self._run_button = Pin(16, Pin.IN, Pin.PULL_DOWN)

        # Multiplexer inputs
        self._mux = MUX(
            ADC(26),
            Pin(27, Pin.OUT, value=1), # MUX enable
            Pin(21, Pin.OUT, value=0), # S0
            Pin(20, Pin.OUT, value=0), # S1
            Pin(19, Pin.OUT, value=0), # S2
            Pin(18, Pin.OUT, value=0)  # S3
        )

        """Primary SPI bus used to communicate with breakout devices
            - MAX31865 (x2) for RTD amplification
            - ST7735 (x1) LED panel driver board 
        """
        if spi:
            self._spi = spi
        else:
            self._spi = SoftSPI(
                baudrate=2000000,
                polarity=0,
                phase=0,    
                sck=Pin(2),
                mosi=Pin(3),
                miso=Pin(4)
            )

    # @property