import machine
import time

PUMP = 28

pump = machine.Pin(28, machine.Pin.OUT, value=0)

if __name__ == "__main__":
    print("starting pump in 3")

    t = 3
    while t > 0:
        time.sleep(1)
        t -= 1
        print(t)

    print("running for 2 seconds")

    pump(1)

    time.sleep(2)

    print("done...")

    pump(0)
