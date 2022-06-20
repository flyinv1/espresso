
from PyQt6.QtWidgets import (
    QWidget
)

class VirtualInstrumentPanel:

    def __init__(self, app):
        self.app = app
        self.window = QWidget()
        self.layout_instruments()

    def layout_instruments(self):
        pass

    def update(self):
        pass

    def close(self):
        self.window.close()

    def show(self):
        self.window.show()