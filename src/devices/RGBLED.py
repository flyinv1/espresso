
class RGBLED:

    def __init__(self, r_pin, g_pin, b_pin):
        self.r_pin = r_pin
        self.g_pin = g_pin
        self.b_pin = b_pin

    def setRedPin(self, pin):
        pass

    def setGreenPin(self, pin):
        pass

    def setBluePin(self, pin):
        pass

    def setColor(self, color):
        # The rgb led can output one color at a time
        # Therefore the inputs to this function are limited to the enum R, G, or B
        # TODO: experiment with mixing colors based on output frequency?
        self.color = color

    def setFrequency(self, frequency):
        pass

    def clearColor(self):
        pass

    def clearFrequency(self):
        pass

    def clear(self):
        self.clearColor()
        self.clearFrequency()

    
