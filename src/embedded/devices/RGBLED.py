import machine

class RGBLED:

    def __init__(self, r_pin, g_pin, b_pin):
        r_pin = machine.Pin(r_pin, machine.Pin.OUT) 
        g_pin = machine.Pin(g_pin, machine.Pin.OUT)
        b_pin = machine.Pin(b_pin, machine.Pin.OUT)

        self.r = machine.PWM(r_pin)
        self.g = machine.PWM(g_pin)
        self.b = machine.PWM(b_pin)

        self.r.freq(1000)
        self.g.freq(1000)
        self.b.freq(1000)

        self.r.duty_u16(int(0))
        self.g.duty_u16(int(0))
        self.b.duty_u16(int(0))

    def set(self, r, g, b):
        # The rgb led can output one color at a time
        # Therefore the inputs to this function are limited to the enum R, G, or B
        # TODO: experiment with mixing colors based on output frequency?
        self.r.duty_u16(int(r / 255 * 2**16))
        self.g.duty_u16(int(g / 255 * 2**16))
        self.b.duty_u16(int(b / 255 * 2**16))

    def on(self):
        self.r.duty_u16(255)
        self.g.duty_u16(255)
        self.b.duty_u16(255)

    def off(self):
        self.r.duty_u16(0)
        self.g.duty_u16(0)
        self.b.duty_u16(0)

    
