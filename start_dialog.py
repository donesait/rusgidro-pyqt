from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import pyqtSignal, QPoint

from utils import resource_path
from video_player import MediaPlayer


class StartDialog(QtWidgets.QDialog):
    start_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(resource_path('ui', 'start_dialog.ui'), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle('Гимнастика')

        self.ui.cancel_button.clicked.connect(self.cancel_clicked.emit)
        self.ui.cancel_button.dragPos = QPoint()
        self.ui.start_button.clicked.connect(self.start_clicked.emit)
        self.ui.start_button.dragPos = QPoint()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # def mousePressEvent(self, event):
    #     if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
    #         self.dragPos = event.globalPosition().toPoint()
    #
    # def mouseMoveEvent(self, event):
    #     if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
    #         self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
    #         self.dragPos = event.globalPosition().toPoint()
    #         event.accept()
