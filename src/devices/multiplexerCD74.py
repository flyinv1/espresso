import machine
import numpy as np

class MultiplexerCD74():

    ADDR_LEN = 16

    def __init__(self, adc, d1, d2, d3, d4, en):
        # d1, d2, d3, d4 select multiplexer address
        # en is enable - the enable pin can be tied to ground to keep the multiplexer always on
        self.adc = machine.ADC(adc)
        self.d1 = machine.Signal(d1, invert=False)
        self.d2 = machine.Signal(d2, invert=False)
        self.d3 = machine.Signal(d3, invert=False)
        self.d4 = machine.Signal(d4, invert=False)
        if en is not None:
            self.enable = machine.Signal(en, invert=True)
        self.selector = (self.d1, self.d2, self.d3, self.d4)

        self.data = np.zeros(self.ADDR_LEN)

    def read(self):
        self.sample_all()
        return self.data

    def sample_all(self):
        for i, addr in enumerate(range(self.ADDR_LEN)):
            self.data[i] = self.sample_addr(addr)

    def sample_addr(self, addr):
        if self.enable:
            self.enable.on()
        if addr < 0 or addr > self.ADDR_LEN:
            # invalid address
            pass

        addr_sel = bin(addr)

        # Set output address
        # address is specified by setting d1-4 in binary
        for i, sig in enumerate(self.selector):
            sig.on() if addr_sel[-i] else sig.off()

        return self.adc.read_u16()
