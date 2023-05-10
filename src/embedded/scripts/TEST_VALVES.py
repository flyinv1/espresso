import machine
import time

RUN_SV = 9
FILL_SV = 13
STEAM_SV = 12

if __name__ == "__main__":

    run_valve = machine.Pin(RUN_SV, machine.Pin.OUT, value=0)
    fill_valve = machine.Pin(FILL_SV, machine.Pin.OUT, value=0)
    steam_valve = machine.Pin(STEAM_SV, machine.Pin.OUT, value=0)
    
    time.sleep(1)

    print("run valve: (open)")
    run_valve(1)

    time.sleep(1)
    print("run valve (closed)")
    run_valve(0)

    time.sleep(1)

    print("fill valve: (open)")
    fill_valve(1)

    time.sleep(1)
    print("fill valve (closed)")
    fill_valve(0)

    time.sleep(1)

    print("steam valve: (open)")
    steam_valve(1)

    time.sleep(1)
    print("steam valve (closed)")
    steam_valve(0)

    time.sleep(0.5)

    print("Done with clicks")

    

