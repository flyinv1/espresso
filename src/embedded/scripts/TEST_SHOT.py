import machine
import time
from devices import multiplexerCD74 as MUX
from devices.MAX31865 import MAX31865

pump = machine.Pin(28, machine.Pin.OUT, value=0)
run_valve = machine.Pin(9, machine.Pin.OUT, value=0)
group_heater = machine.Pin(10, machine.Pin.OUT, value=0)
run_button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)

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


if __name__ == "__main__":

    print("Running integrated test")
    time.sleep(0.25)

    print("Warming Group")
    group_heater(1)

    t = 5
    dt = 0.5
    while t > 0:
        t -= dt
        print(T_boiler.temp(), T_group.temp())
        time.sleep(dt)

    print("Waiting for user input...")

    t_init = time.ticks_ms()
    t_last = t_init
    t_print = t_init
    t_meas = None
    while True:
        if (time.ticks_ms() - t_print) / 1000 > 1:
            data = mux.read()
            print(to_psi(data[4], 300), to_psi(data[5], 60), T_group.temp(), T_boiler.temp())
            t_print = time.ticks_ms()

        if (time.ticks_ms() - t_last) / 1000 > 30:
            print("Waiting for user input...")
            t_last = time.ticks_ms()

        if (time.ticks_ms() - t_init) / 1000 > 600:
            print("Too long!, turning off... :(")
            group_heater(0)
            pump(0)
            run_valve(0)
            exit()
        
        if run_button.value() and t_meas is None:
            t_meas = time.ticks_ms()
            continue
        elif run_button.value() and (time.ticks_ms() - t_meas) < 20:
            continue
        elif run_button.value() and (time.ticks_ms() - t_meas) > 20:
            break

        time.sleep(0.01)

    print("\n\n\n")

    print("Starting pump in 3")
    t = 3
    while t > 0:
        t -= 1
        time.sleep(1)
        print(t)

    group_heater(1)
    run_valve(1)
    time.sleep(0.5)
    pump(1)

    t = 5
    while t > 0:
        t -= 0.05
        time.sleep(0.05)
        data = mux.read()
        print("P: ", to_psi(data[4], _range=300))

    run_valve(0)
    pump(0)

    print("done...")

     