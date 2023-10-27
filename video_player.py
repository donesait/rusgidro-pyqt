from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QPushButton, QSlider, QVBoxLayout, QWidget, QHBoxLayout, QStyle


class MediaPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

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
        self.mediaPlayer.mediaStatusChanged.connect(self.media_status_changed)
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    def new_video(self, video_path):
        print(f'new video {video_path}')
        self.mediaPlayer.stop()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.play_button.setEnabled(True)
        self.play()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def stop(self):
        self.mediaPlayer.stop()

    def media_status_changed(self, status):
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.MediaStatus.EndOfMedia:
            print('end reached')
            self.parent.close()

    def media_state_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
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
