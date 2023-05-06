from PyQt5.QtWidgets import (
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget
)
from PyQt5.QtCore import (
    QSize,
    Qt
)

class QScrollLabel(QScrollArea):

    def __init__(self):
        super().__init__()

        self.setWidgetResizable(True)
        self.widget = QWidget()
        self.setWidget(self.widget)

        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label.setCursor(Qt.IBeamCursor)

        self.layout.addWidget(self.label)
        self.widget.setLayout(self.layout)

        self._autoscroll = True

    def setAutoscroll(self, enabled: bool):
        self._autoscroll = enabled

    def appendLine(self, text):
        self.label.setText(self.label.text() + "\n" + text)
        if self._autoscroll:
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
    