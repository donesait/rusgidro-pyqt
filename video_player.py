from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtWidgets import QPushButton, QSlider, QVBoxLayout, QWidget, QHBoxLayout, \
    QStatusBar, QStyle


class MediaPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mediaPlayer = QMediaPlayer()
        self.audio_output = QAudioOutput()

        btn_size = QSize(16, 16)
        video_widget = QVideoWidget()
        self.setMinimumSize(QSize(640, 480))

        self.setWindowTitle("Гимнастика")

        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setFixedHeight(24)
        self.play_button.setIconSize(btn_size)
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self.play)

        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)

        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.position_slider)

        layout = QVBoxLayout()
        layout.addWidget(video_widget)
        layout.addLayout(control_layout)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(video_widget)
        self.mediaPlayer.setAudioOutput(self.audio_output)
        self.mediaPlayer.playbackStateChanged.connect(self.media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.errorChanged.connect(self.handle_error)

    def new_video(self, video_path):
        self.mediaPlayer.setSource(QUrl.fromLocalFile(video_path))
        self.play_button.setEnabled(True)
        self.play()

    def play(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def media_state_changed(self, state):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
        else:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))

    def position_changed(self, position):
        self.position_slider.setValue(position)

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def handle_error(self):
        self.play_button.setEnabled(False)
        self.status_bar.showMessage("Error: " + self.mediaPlayer.errorString())
