import machine
import time

from devices.MAX31865 import MAX31865

spi = machine.SPI(
    0,
    baudrate=115200,
    polarity=0,
    phase=0,    
    sck=machine.Pin(2),
    mosi=machine.Pin(3),
    miso=machine.Pin(4)
)

T1_CS = 5
T2_CS = 6

T1 = MAX31865(spi, machine.Pin(T1_CS, machine.Pin.OUT))
T2 = MAX31865(spi, machine.Pin(T2_CS, machine.Pin.OUT))

T1.enable_3wire(False)
T2.enable_3wire(False)

while True:
    print(T1.resistance(), T2.resistance(), T1.temp(), T2.temp())
    time.sleep(1)

