import machine
import time
from devices import multiplexerCD74 as MUX

pump = machine.Pin(28, machine.Pin.OUT, value=0)
fill_valve = machine.Pin(13, machine.Pin.OUT, value=0)
steam_valve = machine.Pin(12, machine.Pin.OUT, value=0)

led = machine.Pin(25, machine.Pin.OUT)
led(1)

def to_psi(raw, _range):
    return (raw * 3.3 / 2**15 - 0.65) * _range / (3.3 - 0.65)

mux = MUX.MultiplexerCD74(
    machine.ADC(26),
    machine.Pin(27, machine.Pin.OUT, value=1),
    machine.Pin(21, machine.Pin.OUT, value=0),
    machine.Pin(20, machine.Pin.OUT, value=0),
    machine.Pin(19, machine.Pin.OUT, value=0),
    machine.Pin(18, machine.Pin.OUT, value=0)
)

if __name__ == "__main__":

    print("Running fill test")

    data = mux.read()

    print("P: ", to_psi(data[5], _range=60))

    print("starting fill")

    time.sleep(0.5)

    steam_valve(1)
    print("steam open")

    time.sleep(0.5)

    fill_valve(1)
    print("fill open")

    print("Starting pump in 3")
    t = 3
    while t > 0:
        t -= 1
        time.sleep(1)
        print(t)

    pump(1)

    t = 3
    while t > 0:
        t -= 0.1
        time.sleep(0.1)
        data = mux.read()
        print("P: ", to_psi(data[5], _range=60))

    pump(0)

    while t > 10:
        t -= 0.1
        time.sleep(0.1)
        data = mux.read()
        print("P: ", to_psi(data[5], _range=60))

    fill_valve(0)

    time.sleep(1)
    steam_valve(0)

    print("done...")



