import os.path

from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import pyqtSignal

from constants import ROOT_DIR


class StartDialog(QtWidgets.QDialog):
    start_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()

    def __init__(self, video_id):
        super().__init__()
        self.ui = uic.loadUi(os.path.dirname(__file__) + './ui/start-dialog.ui', self)
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle('Гимнастика')
        # self.video_player = video_player
        if not os.path.exists('videos'):
            os.mkdir('videos')
        if not os.path.exists(f'{ROOT_DIR}/videos/{video_id}.mp4'):
            self.close()

        self.ui.cancel_button.clicked.connect(self.cancel_clicked.emit())
        self.ui.start_button.clicked.connect(self.start_clicked.emit())
        # self.ui.cancel_button.clicked.connect(self.close)
        # self.ui.start_button.clicked.connect(lambda: self.run_player(f'{ROOT_DIR}/videos/{video_id}.mp4'))

    # def run_player(self, video_path):
    #     self.video_player.showMaximized()
    #     self.video_player.new_video(video_path)
    #     self.hide()

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos)
        self.dragPos = event.globalPosition().toPoint()
        event.accept()
