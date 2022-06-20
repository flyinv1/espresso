
from os import sys
from PyQt6.QtWidgets import (
    QWidget, 
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QDial,
    QLabel,
    QSpacerItem,
)
from PyQt6.QtCore import (
    QSize,
    Qt
)

def buildDialPanel(label: str, range: tuple, size=(80, 80)):
    # Convenience method to build a panel for dials

    panel = QVBoxLayout()
    label = QLabel(label)
    dial = QDial()

    label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

    dial.setRange(*range)
    dial.setNotchesVisible(True)
    dial.setFixedSize(*size)

    panel.addWidget(label)
    panel.addWidget(dial)

    return panel, label, dial

class VirtualControlPanel:
    def __init__(self, app):
        self.app = app
        self.window = QWidget()
        self.layout_controller()

    def layout_controller(self):

        self.window.setFixedWidth(300)
        self.windowLayout = QVBoxLayout()

        self.displayLayout = QVBoxLayout()
        self.display = QLabel("")
        self.display.setFixedHeight(200)
        self.display.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.display.setStyleSheet("background: black; color: white;")
        self.display.setContentsMargins(10, 10, 10, 10)
        self.displayLayout.addWidget(self.display)

        self.shotButtonLayout = QVBoxLayout()
        self.rgbLED = QLabel()
        self.rgbLED.setFixedHeight(10)
        self.rgbLED.setStyleSheet("background: blue;")
        self.shotButton = QPushButton()
        self.shotButton.setText("Pull")
        self.shotButtonLayout.addWidget(self.rgbLED)
        self.shotButtonLayout.addWidget(self.shotButton)

        self.switchPanel = QHBoxLayout()
        self.machineEnableSwitch = QPushButton(checkable=True, text="Machine")
        self.boilerEnableSwitch = QPushButton(checkable=True, text="Boiler")
        self.switchPanel.addWidget(self.machineEnableSwitch)
        self.switchPanel.addWidget(self.boilerEnableSwitch)

        self.boilerPanel = QVBoxLayout()
        self.boilerDials = QHBoxLayout()
        self.boilerLabel = QLabel("Boiler")
        self.boilerLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        panel, label, dial = buildDialPanel("P (psi)", (10, 30))
        self.boilerPressureDial = dial
        self.boilerPressureLabel = label
        self.boilerPressurePanel = panel
        self.boilerDials.addLayout(self.boilerPressurePanel)

        panel, label, dial = buildDialPanel("T (°C)", (70, 130))
        self.boilerTemperatureDial = dial
        self.boilerTemperatureLabel = label
        self.boilerTemperaturePanel = panel
        self.boilerDials.addLayout(self.boilerTemperaturePanel)

        self.boilerPanel.addWidget(self.boilerLabel)
        self.boilerPanel.addLayout(self.boilerDials)
        
        self.groupheadPanel = QVBoxLayout()
        self.groupheadDials = QHBoxLayout()
        self.groupheadLabel = QLabel("Grouphead", alignment=Qt.AlignmentFlag.AlignHCenter)

        panel, label, dial = buildDialPanel("P (psi)", (100, 150))
        self.groupheadPressureDial = dial
        self.groupheadPressureLabel = label
        self.groupheadPressurePanel = panel
        self.groupheadDials.addLayout(panel)

        panel, label, dial = buildDialPanel("T (°C)", (70, 100))
        self.groupheadTemperatureDial = dial
        self.groupheadTemperatureLabel = label
        self.groupheadTemperaturePanel = panel
        self.groupheadDials.addLayout(panel)

        self.groupheadPanel.addWidget(self.groupheadLabel)
        self.groupheadPanel.addLayout(self.groupheadDials)

        self.windowLayout.addLayout(self.displayLayout)
        self.windowLayout.addLayout(self.shotButtonLayout)
        self.windowLayout.addLayout(self.groupheadPanel)
        self.windowLayout.addLayout(self.boilerPanel)
        self.windowLayout.addItem(QSpacerItem(1, 24))
        self.windowLayout.addLayout(self.switchPanel)

        self.shotButton = QPushButton()

        self.MachineDisplayLabel = QLabel()

        # self.windowLayout.addChildLayout(self.switchPanel)

        self.window.setBaseSize(QSize(400, 720))
        self.window.setLayout(self.windowLayout)
        self.window.setWindowTitle("Virtual Control Panel")

    def connect(self, io):
        self.boilerPressureDial.valueChanged.connect(io.boilerPressureCommandSignal.update)
        self.boilerTemperatureDial.valueChanged.connect(io.boilerTemperatureCommandSignal.update)
        self.groupheadPressureDial.valueChanged.connect(io.groupheadPressureCommandSignal.update)
        self.groupheadTemperatureDial.valueChanged.connect(io.groupheadTemperatureCommandSignal.update)
        
        # Switches require special treatment because pressed/released are different calls
        self.machineEnableSwitch.pressed.connect(lambda: io.machineEnableCommandSignal.update(1))
        self.machineEnableSwitch.released.connect(lambda: io.machineEnableCommandSignal.update(0))
        self.boilerEnableSwitch.pressed.connect(lambda: io.boilerEnableCommandSignal.update(1))
        self.boilerEnableSwitch.released.connect(lambda: io.boilerEnableCommandSignal.update(0))
        self.shotButton.pressed.connect(lambda: io.shotEnableCommandSignal(1))
        self.shotButton.released.connect(lambda: io.shotEnableCommandSignal(0))

        # TODO Hacky way to set initial values... :(
        self.boilerPressureDial.valueChanged.emit(self.boilerPressureDial.value())
        self.boilerTemperatureDial.valueChanged.emit(self.boilerTemperatureDial.value())
        self.groupheadPressureDial.valueChanged.emit(self.groupheadPressureDial.value())
        self.groupheadTemperatureDial.valueChanged.emit(self.groupheadTemperatureDial.value())

    def close(self):
        self.window.close()

    def show(self):
        self.window.show()
