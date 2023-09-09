import os.path

from PyQt6 import QtCore, QtWidgets, uic
from PyQt6.QtCore import pyqtSignal, QPoint

from constants import root_dir
from utils import resource_path
from video_player import MediaPlayer


class StartDialog(QtWidgets.QDialog):
    start_clicked = pyqtSignal()
    cancel_clicked = pyqtSignal()

    def __init__(self, video_id):
        super().__init__()
        self.ui = uic.loadUi(resource_path('ui', 'start_dialog.ui'), self)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle('Гимнастика')
        if not os.path.exists('videos'):
            os.mkdir('videos')
        if not os.path.exists(f'{root_dir}/videos/{video_id}.mp4'):
            self.close()

        self.ui.cancel_button.clicked.connect(self.reject)
        self.ui.cancel_button.dragPos = QPoint()
        self.ui.start_button.clicked.connect(self.accept)
        self.ui.start_button.dragPos = QPoint()

    def close(self) -> bool:
        return super().close()

    def accept(self):
        super().accept()

    def reject(self):
        super().reject()

    def run_player(self, video_path):
        video_player = MediaPlayer()
        video_player.showMaximized()
        video_player.new_video(video_path)

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
