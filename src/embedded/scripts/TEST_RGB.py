import machine
import time
import math

if __name__ == "__main__":

    r = machine.PWM(machine.Pin(17, machine.Pin.OUT))
    g = machine.PWM(machine.Pin(15, machine.Pin.OUT))
    b = machine.PWM(machine.Pin(14, machine.Pin.OUT))

    r.freq(int(1e5))
    g.freq(int(1e5))
    b.freq(int(1e5))

    # r.init(freq=1e5, duty_u16=0)
    # g.init(freq=1e5, duty_u16=0)
    # b.init(freq=1e5, duty_u16=0)
    
    on = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)

    time.sleep(1)
    print("red")
    r.duty_u16(2**15)
    time.sleep(1)
    print("green")
    r.duty_u16(0)
    g.duty_u16(2**15)
    time.sleep(1)
    print("blue")
    g.duty_u16(0)
    b.duty_u16(2**15)
    time.sleep(1)
    b.duty_u16(0)

    while True:

        time.sleep(0.001)

        t = time.ticks_ms()

        # r.duty_u16(int(math.sin(t / 1000) + 1) * 2**15)
        # g.duty_u16(int(math.sin(t / 1600) + 1) * 2**15)
        # b.duty_u16(int(math.sin(t / 2000) + 1) * 2**15)

        if on.value():
            r.duty_u16(2**15)

        else:
            r.duty_u16(0)