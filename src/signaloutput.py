
class SignalOutput:
    # The default SignalOutput class is an abstract template
    #   Subclasses will implement hardware specific methods
    #   All signal outputs must implement the `write` and `latest` functions

    def __init__(self):
        self.current = 0.0

    def latest(self):
        return self.current

    def write(self, value):
        self.current = value
