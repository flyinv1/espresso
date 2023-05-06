import machine
import time
from sys import stdin
import gc
import json
from select import poll, POLLIN
import math
import random

from devices.multiplexerCD74 import MultiplexerCD74
from devices.RGBLED import RGBLED
import devices.MAX31865 as RTD

# # These colors don't represent the real RGB color
# # They are 'perceived' output from the LED, since it 
# # is largely dominated by red
orange = (200, 255, 0)
# # blue = (20, 120, 255)
# # green = (60, 255, 120)

# # # Frequency
datarate = 5

devices = {
    "IO-00": machine.Pin(25, machine.Pin.OUT),
    "SV-00": machine.Pin(9, machine.Pin.OUT),
    "SV-01": machine.Pin(14, machine.Pin.OUT),
    "SV-02": machine.Pin(15, machine.Pin.OUT),
    "HT-00": machine.Pin(8, machine.Pin.OUT),
    "HT-01": machine.Pin(7, machine.Pin.OUT)
}

sensors = {
    "PT-00": 0,
    "PT-01": 1,
    "PT-02": 2,
}

# mux = MultiplexerCD74(26, 2, 6, 5, 4, 3)
# mux = MultiplexerCD74(
#     machine.ADC(0),
#     machine.Pin(27, machine.Pin.OUT, value=1), 
#     machine.Pin(10, machine.Pin.OUT, value=0), 
#     machine.Pin(11, machine.Pin.OUT, value=0), 
#     machine.Pin(12, machine.Pin.OUT, value=0), 
#     machine.Pin(13, machine.Pin.OUT, value=0)
# )

poller = poll()

# def command_device(device_id, value):
#     try:
#         devices[device_id].value(bool(value))
#     except Exception:
#         print("man...")

# def poll_input():
#     if poller.poll(0):
#         data = stdin.readline()
#         payload = json.loads(data)
#         try:
#             if "route" in payload.keys():
#                 route = payload["route"]
#                 if route == "cmd":
#                     for device_id, value in payload["data"].items():
#                         command_device(device_id, value)
#                 elif route == "sample":
#                     if "device_id" in payload["data"]:
#                         # m = mux.sample_addr(payload["data"]["device_id"])
#                         print(f"{3.3*m/2**16:5.2f}")
#                     else:
#                         # m = mux.read()
#                         print("\t".join([f"{3.3*d/2**16:5.2f}" for d in m]))
#                 elif route == "set/datarate":
#                     if payload["data"]:
#                         datarate = payload["data"]
#                 elif route == "set/profile":
#                     pass
#                 elif route == "get/profile":
#                     pass
#                 elif route == "del/profile":
#                     pass
#                 elif route == "list/devices":
#                     pass
#                 elif route == "list/sensors":
#                     pass
#                 else:
#                     pass
#             else:
#                 print("expected something...")
#         except Exception:
#             print("Malformed message")


if __name__ == "__main__":

    spi = machine.SoftSPI(
                  baudrate=115200, 
                  polarity=0,
                  phase=0,
                  sck=machine.Pin(2), 
                  mosi=machine.Pin(3), 
                  miso=machine.Pin(4))

    rtd_boiler = RTD.MAX31865(spi=spi, cs=machine.Pin(5, machine.Pin.OUT, value=1))
    rtd_group = RTD.MAX31865(spi=spi, cs=machine.Pin(6, machine.Pin.OUT, value=1))

    

# #     # Loop index
#     i = 0
#     t = 0
#     t_last = 0

#     while True:
#         i += 1
#         t = time.ticks_ms()
#         if (t - t_last) / 1000 > (1 / datarate):
#             t_last = t

#             print(rtd_boiler.resistance(), rtd_boiler.temp())
#             print(rtd_group.resistance(), rtd_group.temp())
            
#             rgb = RGBLED(18, 19, 20)
#             rgb.set(*orange)

#             # m = mux.read()
#             # print("\t".join(["{:05d}".format(_m) for _m in m]))


#     # print("okay")

#     # # Loop index
#     # i = 0
#     # t = 0
#     # t_last = 0

#     # pump_pwm_freq = 10000

#     # pump = machine.PWM(machine.Pin(23, machine.Pin.OUT))    
#     # pump.freq(pump_pwm_freq)
#     # pump.duty_u16(0)
    
#     # pwm_rate = 0

#     # for device in devices.values():
#     #     device.value(0)

#     # while True:
#     #     i += 1
#     #     t = time.ticks_ms()
#     #     if (t - t_last) / 1000 > 1 / datarate:
#     #         t_last = t
#     #         m = mux.read() 
#     #         # duty_cyc = min(max(int(m[0]), 0), 65535)
#     #         duty_cyc = int(m[0])
#     #         pump.duty_u16(duty_cyc)
#     #         # print(duty_cyc)

#     #         print(rtd.temp())

#     #         # print("\t".join([f"{3.3*d/2**16:5.2f}" for d in m]))



#     #     poll_input()

