from PyQt5.QtWidgets import (
    QLabel,
    QBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QListWidget,
    QVBoxLayout,
    QGridLayout,
    QListWidgetItem,
    QLineEdit,
)
from PyQt5.QtCore import (
    QSize,
    pyqtSignal
)
from PyQt5.QtGui import (
    QIntValidator
)
import enum
from serial.tools.list_ports import comports


class QSerialWidgetDisplayState(enum.Enum):
    DISCONNECTED = enum.auto()
    CONNECTED = enum.auto()

class QSerialWidget(QWidget):
    """Each widget can connect to only a single serial port"""
    
    openClicked = pyqtSignal(str, int)
    closeClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setMaximumWidth(296)
        self.setMinimumWidth(296)

        self.connected = False
        self.state = QSerialWidgetDisplayState.DISCONNECTED
        self.port: str = None
        self.baud: int = 115200
        self.ports: list = []

        self.refreshButton = QPushButton("Refresh")
        self.refreshButton.clicked.connect(self._refreshConnections)

        self.connectButton = QPushButton("Connect")
        self.connectButton.clicked.connect(self._onRequestConnection)
        self.connectButton.setDisabled(True)

        self.baudInput = QLineEdit()
        self.baudInput.setToolTip("Connection baud rate (bits per second)")
        self.baudInput.setValidator(QIntValidator())
        self.baudInput.setText("115200")
        self.baudInput.textEdited.connect(self._setBaud)

        self.inputGrid = QGridLayout()
        self.inputGrid.addWidget(QLabel("Baud"), 0, 0)
        self.inputGrid.addWidget(self.baudInput, 0, 1)

        self.connectionList = QListWidget()
        self.connectionList.itemClicked.connect(self._selectSerialConnectionByRow)

        self.layout = QVBoxLayout()

        self.inputs = QWidget()
        self.inputLayout = QVBoxLayout()
        self.inputLayout.addWidget(QLabel("Serial Connection"))
        self.inputLayout.addLayout(self.inputGrid)
        self.inputLayout.addWidget(self.refreshButton)
        self.inputLayout.addWidget(self.connectionList)
        self.inputs.setLayout(self.inputLayout)

        self.layout.addWidget(self.inputs)
        self.layout.addWidget(self.connectButton)

        self.setLayout(self.layout)

        self._refreshConnections()


    def setDisplayState(self, state: QSerialWidgetDisplayState):
        self.state = state
        if state == QSerialWidgetDisplayState.CONNECTED:
            self.connected = True
            self.inputs.setEnabled(False)
            self.connectButton.setText("Disconnect")
        elif state == QSerialWidgetDisplayState.DISCONNECTED:
            self.connected = False
            self.inputs.setEnabled(True)
            self.connectButton.setText("Connect")

    def _onRequestConnection(self):
        if not self.connected:
            self.openClicked.emit(self.port, self.baud)
        else:
            self.closeClicked.emit()

    def _selectSerialConnectionByRow(self, item: QListWidgetItem):
        self.connectButton.setEnabled(True)
        self.port = item.text()

    def _setBaud(self, value):
        try:
            print(value)
            self.baud = int(value)
        except Exception as E:
            print(E)

    def _refreshConnections(self):
        self.ports = comports()
        for i in range(self.connectionList.count()):
            self.connectionList.takeItem(i)
        self.connectionList.addItems([ c.device for c in self.ports ])
        self.update()

