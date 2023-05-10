import machine
import time

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

# bin_map = [
#     [0, 0, 0, 0],
#     [1, 0, 0, 0],
#     [0, 1, 0, 0],
#     [1, 1, 0, 0],
#     [0, 0, 0, 1],
#     [1, 0, 0, 1],
#     [0, 1, 0, 1],
#     [1, 1, 0, 1],
#     [0, 0, 1, 0],
#     [1, 0, 1, 1],
#     [0, 1, 1, 0],
#     [1, 1, 1, 0],
#     [0, 0, 1, 1],
#     [1, 0, 1, 1],
#     [0, 1, 1, 1],
#     [1, 1, 1, 1],
# ]

class MultiplexerCD74():

    ADDR_LEN = int(16)

    def __init__(self, adc, en, d1, d2, d3, d4):
        # d1, d2, d3, d4 select multiplexer address
        # en is enable - the enable pin can be tied to ground to keep the multiplexer always on
        self.adc = adc
        self.enable = en
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        self.d4 = d4
        
        self.selector = [
            self.d1, 
            self.d2, 
            self.d3, 
            self.d4
        ]

        self.data = [0.0] * self.ADDR_LEN

    def read(self):
        self.enable(0)
        self.sample_all()
        self.enable(1)
        return self.data


    def sample_all(self):
        for i in range(self.ADDR_LEN):
            self.data[i] = self.sample_addr(i)

    def sample_addr(self, addr, latch_pins=False):

        if addr < 0 or addr >= self.ADDR_LEN:
            return 0.0 # Invalid address

        # num = addr
        # binary_arr = []
        # while num != 0:
        #     binary_arr.insert(0, num % 2)
        #     num = num // 2

        # # Pad the binary array to a length of 4
        # while len(binary_arr) < 4:
        #     binary_arr.insert(0, 0)

        binary_arr = bin_map[addr]

        # print(addr, binary_arr)

        # binary_arr.reverse()

        for i, pin in enumerate(self.selector):
            pin(1) if binary_arr[3 - i] else pin(0)
                
        value = self.adc.read_u16()

        if not latch_pins:
            self.reset()

        return value


    def reset(self):
        for pin in self.selector:
            pin(0)