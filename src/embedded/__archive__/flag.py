
class FlagManager:
    def __init__(self):
        self.flags = []

    def healthy(self):
        return True

    def redlineLow(self, *args, **kwargs):
        print(*args)

    def redlineHigh(self, *args, **kwargs):
        print(*args)
