import machine
import time

from devices.MAX31865 import MAX31865
from devices import multiplexerCD74 as MUX

def to_psi(raw, _range):
    return (raw * 3.3 / 2**15 - 0.65) * _range / (3.3 - 0.65)

led = machine.Pin(25, machine.Pin.OUT)
led(1)

fill_valve = machine.Pin(13, machine.Pin.OUT, value=0)
steam_valve = machine.Pin(12, machine.Pin.OUT, value=0)
boiler_heater = machine.Pin(11, machine.Pin.OUT, value=0)

r = machine.PWM(machine.Pin(17, machine.Pin.OUT))
r.freq(int(1e5))

spi = machine.SoftSPI(
    baudrate=115200,
    polarity=0,
    phase=0,    
    sck=machine.Pin(2),
    mosi=machine.Pin(3),
    miso=machine.Pin(4)
)

T_boiler = MAX31865(spi, machine.Pin(5, machine.Pin.OUT))
T_group = MAX31865(spi, machine.Pin(6, machine.Pin.OUT))

mux = MUX.MultiplexerCD74(
    machine.ADC(26),
    machine.Pin(27, machine.Pin.OUT, value=1),
    machine.Pin(21, machine.Pin.OUT, value=0),
    machine.Pin(20, machine.Pin.OUT, value=0),
    machine.Pin(19, machine.Pin.OUT, value=0),
    machine.Pin(18, machine.Pin.OUT, value=0)
)

if __name__ == "__main__":

    print("Starting boiler test...")
    print("Ensure B-EN is on")

    time.sleep(1)

    boiler_heater(1)

    dt = 1
    t = 300
    while t > 0:
        t -= dt
        data = mux.read()
        print(t, to_psi(data[5], _range=60), T_boiler.temp(), T_group.temp())
        r.duty_u16(2**15)
        time.sleep(dt)


    boiler_heater(0)
    steam_valve(1)

    time.sleep(15)

    steam_valve(0)

    print("done...")

    