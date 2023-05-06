from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QPushButton
)

from PyQt5.QtCore import (
    pyqtSignal
)

import enum

class OnOffControl(QWidget):

    toggled = pyqtSignal(str, bool)

    def __init__(self, device_id, name, label="Valve", default=False):
        super().__init__()

        self.on = default
        self.device_id = device_id

        self.valveLabel = QLabel(label)
        self.componentLabel = QLabel(device_id)
        self.nameLabel = QLabel(name)
        self.toggle = QPushButton("CLOSED")
        self.toggle.setFixedWidth(120)
        self.toggle.clicked.connect(self._clicked)

        self.valveLabel.setStyleSheet("color: 'grey'")

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.valveLabel)
        self.layout.addWidget(self.componentLabel)
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.toggle)

        self.setLayout(self.layout)

    def _clicked(self):
        self.on = not self.on
        self.toggle.setText("OPEN" if self.on else "CLOSED")
        self.toggled.emit(self.device_id, self.on)