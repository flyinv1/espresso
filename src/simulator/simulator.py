
from os import sys

from PyQt6.QtWidgets import (
    QApplication
)
from espressomanager import EspressoManager
from .virtualcontrolpanel import VirtualControlPanel
from .virtualinstrumentpanel import VirtualInstrumentPanel
from .virtualiocontroller import VirtualIOController

from .model import FluidModel


class Simulator:
    def __init__(self):

        self.app = QApplication(sys.argv)

        self.model = FluidModel()
        self.controlPanel = VirtualControlPanel(self.app)
        self.instrumentPanel = VirtualInstrumentPanel(self.app)
        
        self.io = VirtualIOController(self.controlPanel)
        self.manager = EspressoManager(self.io)


    def update(self):
        # Order of updates:
        #   1) Fluid model
        #   2) Input Panel
        #   3) Instrument Panel
        #   4) Espresso Manager
        #   
        #   1-3 represent physical systems
        #   4 represents logic updates


        # Fluid model
        self.model.update()

        # Manager logic
        self.manager.update()

        # Update Application windows
        # This order guarantees that inputs will not be processed until the next manager update.
        self.app.processEvents()


    def start(self):
        self.controlPanel.show()
        self.instrumentPanel.show()
        while True:
            self.update()
