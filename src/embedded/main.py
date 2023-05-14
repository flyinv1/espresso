
from machine import (
    Pin, 
    SoftSPI,
    ADC
)

import sys, uselect, time, math

from devices.MAX31865 import MAX31865
from devices.multiplexerCD74 import MultiplexerCD74 as MUX
from devices.RGBLED import RGBLED as rgb
from pid import PID
from machineio import MachineIO


"""Machine States"""
class State():
    standby = "standby" # Default state
    pulling = "pulling" # Shot is being pulled

# Initialize Machine input / ouput
mio = MachineIO()

"""Primary loop frequency"""
f_primary = 1
f_heater = 5
f_pump = 20
dt_primary = 1 / f_primary
dt_heater = 1 / f_heater
dt_pump = 1 / f_pump

"""Input Poll"""
poller = uselect.poll()
poller.register(sys.stdin, uselect.POLLIN)

"""Controllers"""
boiler_pid = PID(1, 0, 0, windup_threshold=100)
group_pid = PID(1, 0, 0, windup_threshold=100)

group_heater_band = 1.25
shot_time = 30 * 1000

def scale(value, default=2**16, min_value=0, max_value=3.3, offset_volts=0.0, reverse=False):
    if reverse:
        return ((default - value) / default - offset_volts) * (max_value - min_value)
    else:
        return ((value - default) / default - offset_volts) * (max_value - min_value)

def to_psi(value, p_range=1):
    # Standard PTs read 0.5 to 4.5V
    # analog output is regulated to 3.3V full scale, which corresponds to
    # 0.33-2.97V of real input (2.64V of range)
    return ((value / 2 ** 16) - 0.33) / 2.64 * p_range

if __name__ == "__main__":

    # Loop controls
    t_last = 0
    t_last_h = 0
    t_last_p = 0
    t_elapsed = 0
    t_pulling = 0

    # Primary loop frequency
    f = 30

    state: State = State.standby

    waiting_for_input = False
    standby_heating = True


    while True:
        t = time.ticks_ms()
        
        if (t - t_last) > 1000 / f_primary:

            # print(T_boiler.temp(), T_group.temp())
            # if T_group.fault:
            #     print(bin(T_group.read_fault()), T_group.read_low_fault(), T_group.read_high_fault())
            
            raw_data = mux.read()
            
            ### Calculate pressures
            # print("\t".join(f"{m:0.2f}" for m in raw_data))

            boiler_temp = T_boiler.temp()
            group_temp = T_group.temp()

            boiler_pressure = to_psi(raw_data[5], p_range=60)
            group_pressure = to_psi(raw_data[6], p_range=300)

            setpoint_group_pressure = scale(raw_data[1], min_value=0, max_value=12, reverse=True)
            setpoint_group_temp = scale(raw_data[0], min_value=0, max_value=100, reverse=True)
            setpoint_boiler_pressure = scale(raw_data[3], min_value=0, max_value=1, reverse=True)
            setpoint_boiler_temp = scale(raw_data[2], min_value=0, max_value=125, reverse=True)

            # print("\t".join(f"{m:0.2f}" for m in [
            #     boiler_pressure,
            #     group_pressure,
            #     setpoint_group_pressure,
            #     setpoint_group_temp,
            #     setpoint_boiler_pressure,
            #     setpoint_boiler_temp
            # ]))

            if state == State.standby:
                # if abs(setpoint_group_temp - group_temp) > group_heater_band:
                #     status_led.set(200, 0, 0)
                # else:
                #     status_led.set(0, 255, 0)

                if (t - t_last_p) > 1000 / f_pump:
                    """Pump code here"""
                    t_last_p = time.ticks_ms()


                if (t - t_last_h) > 1000 / f_heater:
                    """Heater code here"""

                    """Ah, a sad old bang bang"""
                    if group_temp > (setpoint_group_temp + group_heater_band):
                        h_group(0)
                        status_led.set(100, 0, 0)
                    elif group_temp > (setpoint_group_temp - group_heater_band) and not h_group.value():
                        h_group(0)
                        status_led.set(0, 255, 0)
                    elif group_temp > (setpoint_group_temp - group_heater_band) and h_group.value():
                        h_group(1)
                        status_led.set(0, 255, 0)
                    else:
                        h_group(1)
                        status_led.set(100, 0, 0)

                    t_last_h = time.ticks_ms()

                if (run_button.value()) and not waiting_for_input:
                    waiting_for_input = True
                    t_waiting = time.ticks_ms()
                if (run_button.value() and waiting_for_input):
                    if (time.ticks_ms() - t_waiting) > 20:
                        state = State.pulling
                        waiting_for_input = False
                        t_pulling = time.ticks_ms()
                        h_group(0)
                        h_boiler(0)
                        
            elif state == State.pulling:
                t_elapsed = time.ticks_ms() - t_pulling

                pump(1)
                sv_group(1)

                if t_elapsed > shot_time:
                    pump(0)
                    sv_group(0)
                    state = State.standby



            data_frame = [
                t / 1000,
                run_button.value(),
                boiler_pressure,
                group_pressure,
                boiler_temp,
                group_temp,
                setpoint_group_pressure,
                setpoint_group_temp,
                setpoint_boiler_pressure,
                setpoint_boiler_temp
            ]
            

            print("\t".join([f"{m:0.2f}" for m in data_frame]))

            t_last = time.ticks_ms()
             

        


