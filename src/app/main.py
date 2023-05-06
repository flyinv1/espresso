from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
    QPushButton,
    QLineEdit
)
from PyQt5.QtCore import (
    QSize,
    pyqtSlot,
    QIODevice,
    QThread
)
from PyQt5.QtGui import (
    QIntValidator
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo

from src.app.Widgets.SerialWidget import (
    QSerialWidget,
    QSerialWidgetDisplayState
)

from src.app.Widgets.ControlWidgets import (
    OnOffControl
)

from src.app.Widgets.ConsoleWidget import QScrollLabel

import warnings
import serial
import yaml
import json
import enum

class Device(enum.Enum):
    LED = "LED"
    SWITCH = "SW"
    SOLENOID_VALVE = "SV"
    PROPORTIONAL_VALVE = "PV"
    THERMOCOUPLE = "TC"
    PRESSURE_TRANSDUCER = "PT"

with open('./src/api/channels.yml') as f: 
    configuration = yaml.safe_load(f)
    channels = configuration['channels']

def parse_device(code: str):
    c = code.split("-")
    # if len(c) != 2:
    #     warnings.warn(f'Invalid device code -- too many entries. Received {len(c)}, expected 2 for code {code}')
    return (c[0], int(c[1]))

# class SerialThread(QThread):

class Main(QWidget):

    def __init__(self):
        super().__init__()
        
        self.serial_port = None
        self.serial_stream = ""
        self.sample_addr = None

        self.controlRibbon = QHBoxLayout()
        self.serialVisibleButton = QPushButton(">>")
        self.serialVisibleButton.clicked.connect(self._toggleSerialWidget)
        self.controlRibbon.addWidget(self.serialVisibleButton)

        self.serialWidget = QSerialWidget()
        self.serialWidget.openClicked.connect(self._openSerial)
        self.serialWidget.closeClicked.connect(self._closeSerial)
        
        self.layout = QHBoxLayout()

        self.deviceControlWidget = QWidget()
        self.deviceControlWidget.setEnabled(False)
        self.deviceControlLayout = QVBoxLayout()
        self.deviceControlWidget.setLayout(self.deviceControlLayout)

        for channel in channels:
            device = channel['device']
            name = channel['name']
            (_type, *rest) = parse_device(device)
            
            if _type == "SV" or _type == "HT" or _type == "LED":
                label = "Valve" if _type == "SV" else "LED"
                default = 0
                if 'default' in channel: default = channel['default']
                widget = OnOffControl(device, name, label=label, default=default)
                widget.toggled.connect(self._setOnOffDevice)
                self.deviceControlLayout.addWidget(widget)

        self.command_input = QLineEdit()
        # self.command_input.textChanged.connect(self.set_command)
        self.command_button = QPushButton("Sample")
        self.command_button.clicked.connect(self._sample)
        # self.deviceControlLayout.addWidget(self.int_input)
        # self.deviceControlLayout.addWidget(self.int_button)

        self.deviceControlLayout.addStretch()

        self.console = QScrollLabel()
        self.console.setMinimumWidth(100)
        self.console.setMaximumHeight(500)
        
        # self.layout.addWidget()
        self.layout.addLayout(self.controlRibbon)
        self.layout.addWidget(self.deviceControlWidget)
        self.layout.addWidget(self.console)
        self.layout.addWidget(self.serialWidget)

        self.setLayout(self.layout)


    def _openSerial(self, port, baud):
        try:
            self.serial_port = QSerialPort(
                port, 
                baudRate=baud,
                readyRead=self._parseSerial
            )
            if self.serial_port.open(QIODevice.ReadWrite):
                self.serialWidget.setDisplayState(QSerialWidgetDisplayState.CONNECTED)
                self.deviceControlWidget.setEnabled(True)
        except Exception as E:
            print(E)


    def _closeSerial(self):
        try:
            self.serial_port.close()
            self.serialWidget.setDisplayState(QSerialWidgetDisplayState.DISCONNECTED)
            self.deviceControlWidget.setEnabled(False)
        except Exception as E:
            print(E)

    @pyqtSlot()
    def _parseSerial(self):
        while self.serial_port.canReadLine():
            text = self.serial_port.readLine().data().decode()
            text = text.rstrip('\r\n')
            # self.console.appendLine(text)


    def _setOnOffDevice(self, device_id: str, on: bool):
        print(device_id, on)
        self.serial_port.write((json.dumps({
            "route": "cmd",
            "data": {
                device_id: on
            }
        }) + "\n").encode())

    
    def _toggleSerialWidget(self):
        self.serialWidget.setVisible(not self.serialWidget.isVisible())
        self.serialVisibleButton.setText(">>" if self.serialWidget.isVisible() else "<<")

    def _select_addr(self, value):
        try:
            self.sample_addr = int(value)
        except:
            self.sample_addr = None

    def _sample(self):
        self.serial_port.write((json.dumps({
            "route": "sample",
            "data": {"device_id": self.sample_addr}
        }) + "\n").encode())


if __name__ == "__main__":
    import sys
    app = QApplication([])
    main = Main()
    main.show()
    sys.exit(app.exec())