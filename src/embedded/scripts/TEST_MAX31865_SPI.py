from machine import Pin, SPI, SoftSPI
import time

if __name__ == "__main__":

    CONFIG = 0b11010000

    spi = SoftSPI(
        baudrate=115200,
        polarity=0,
        phase=0,
        sck=Pin(2),
        mosi=Pin(3),
        miso=Pin(4)
    )

    cs_0 = Pin(5, Pin.OUT, value=1)
    cs_1 = Pin(6, Pin.OUT, value=1)
    cs = cs_1

    time.sleep(0.005)

    cs(0)
    spi.write(bytes([0x80, CONFIG]))
    cs(1)

    time.sleep(0.001)
    cs(0)
    spi.write(bytes([0x00]))
    config = spi.read(1)[0]
    cs(1)
    print("config: ", bin(config))

    t_last = 0

    f = 10

    while True:
        if (time.ticks_ms() - t_last) > (1000.0 / f):
            cs(0)
            spi.write(bytes([0x01]))
            msb = spi.read(1)[0]
            cs(1)

            time.sleep(0.001)

            cs(0)
            spi.write(bytes([0x02]))
            lsb = spi.read(1)[0]
            cs(1)
            
            # lsb = _b[1]
            err = lsb & 0x01
            cs(1)

            res = ((msb << 7) | (lsb >> 1)) * 430.0 / 2**15
            T = (res / 100.0 - 1.0) / 0.00385

            if err:
                cs(0)
                spi.write(bytes([0x07]))
                _f = spi.read(1)[0]
                print("err: ", bin(_f))
                cs(1)

                cs(0)
                spi.write(bytes([0x80, CONFIG | 0b00000010]))
                cs(1)

            print("data: ", bin(msb), bin(lsb), (msb << 7) | (lsb >> 1), res, T)

            t_last = time.ticks_ms()