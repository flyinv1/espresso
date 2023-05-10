
from machine import Pin, ADC
import time
import utime

if __name__ == "__main__":
    
    bin_map = [
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 1, 0, 0],
        [0, 1, 0, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 1],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
        [1, 0, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 1],
        [1, 1, 1, 0],
        [1, 1, 1, 1],
    ]

    adc = ADC(Pin(26, Pin.IN))
    
    pins = [
        Pin(21, Pin.OUT, value=0),
        Pin(20, Pin.OUT, value=0),
        Pin(19, Pin.OUT, value=0),
        Pin(18, Pin.OUT, value=0)
    ]

    en = Pin(27, Pin.OUT, value=1)

    t_last = 0
    f = 50

    channels = [
        0,
        1,
        2,
        3,
        5,
        6
        # 2,
        # 3
    ]

    while True:

        if (time.ticks_ms() - t_last) > (1000 / f):
            
            en(0)

            data = [0] * len(channels)

            for _i, c in enumerate(channels):
                pin_state = bin_map[c]
                for i, pin in enumerate(pins):
                    pin.value(pin_state[3 - i])
                utime.sleep(0.1)
                data[_i] = adc.read_u16() * 3.3 / 2 ** 16
                # print(adc.read_u16() * 3.3 / 2 ** 16)

            print("\t".join(["{:0.3f}".format(m) for m in data]))

            en(1)

            pins[0].value(0)
            pins[1].value(0)
            pins[2].value(0)
            pins[3].value(0)

            time.sleep(0.1)

            # print(adc.read_u16() * 3.3 / 2 ** 16)

            # for i, p in enumerate(bin_map):
            #     for j, _p in enumerate(p):
            #         pins[3 - j].value(_p)
            #     time.sleep(0.001)
            #     _data[i] = adc.read_u16() * 3.3 / 2**16
            #     time.sleep(0.001)

            # print("\t".join(["{:0.3f}".format(m) for m in _data]))

            t_last = time.ticks_ms()