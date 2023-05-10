import machine
import time

from devices import multiplexerCD74 as MUX

GROUP_PT_INDEX = 4
BOILER_PT_INDEX = 5

def to_psi(raw, _max):
    return (raw * 3.3 / 2**15 - 0.65) * _max / (3.3 - 0.65)

if __name__ == "__main__":

    mux = MUX.MultiplexerCD74(
        machine.ADC(26),
        machine.Pin(27, machine.Pin.OUT, value=1),
        machine.Pin(21, machine.Pin.OUT, value=0),
        machine.Pin(20, machine.Pin.OUT, value=0),
        machine.Pin(19, machine.Pin.OUT, value=0),
        machine.Pin(18, machine.Pin.OUT, value=0)
    )

    t = 0
    f = 1

    while True:
        if time.ticks_ms() - t > 1000 / f:
            
            d = mux.read()
            print("\t".join(["{:0.2f}".format(_d * 3.3 / 2 ** 15) for _d in d]))
            print(to_psi(d[GROUP_PT_INDEX], 300))
            print(to_psi(d[BOILER_PT_INDEX], 60))

            print("\n--\n")

            t = time.ticks_ms()

