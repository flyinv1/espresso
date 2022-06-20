
class VirtualSignal:

    def __init__(self):
        self.current = 0.0
        self.listeners = []

    def update(self, value):
        self.current = value
        [ listener(self.current) for listener in self.listeners ]

    def connect(self, listener):
        self.listeners.append(listener)

    def value(self):
        return self.current
