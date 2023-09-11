import asyncio
import os
import sys
from typing import Optional, Dict, List

from PyQt6 import QtGui

from schedule import VideoSchedule
from datetime import datetime, timedelta

from qasync import QEventLoop, asyncSlot
from PyQt6.QtCore import QTimer, QSize
from PyQt6.QtGui import QResizeEvent, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow

from dto import Training
from start_dialog import StartDialog
from utils import resource_path, video_path, periodic
from video_player import MediaPlayer
from videos import Videos


@asyncSlot()
@periodic(5 * 60)
async def periodic_update_schedule(window):
    print('update schedule')
    schedule_task = window.loop.run_in_executor(None, VideoSchedule.update_data)
    await schedule_task
    window.schedule = VideoSchedule.dict_by_day


@asyncSlot()
@periodic(20 * 60)
async def periodic_download_videos(window):
    print('download_videos')
    download_task = window.loop.run_in_executor(None, Videos.download_all)
    await download_task
    window.downloaded_video = Videos.downloaded_video


class MainWindow(QMainWindow):
    minimum_show_interval = timedelta(minutes=0)
    last_show_time = None

    def __init__(self, loop=None):
        super().__init__()

        videos_dir = resource_path('videos')
        if not os.path.exists(videos_dir):
            os.mkdir(videos_dir)
        Videos.check_videos()

        self.window_opened = False
        self.dialog_opened = False

        self.schedule: Optional[Dict[int, List[Training]]] = None
        self.downloaded_video: Optional[Dict[int, bool]] = None

        self.setWindowTitle('Гимнастика')
        self.setWindowIcon(QIcon(resource_path('assets', 'rg_logo.ico')))
        self.setMinimumSize(QSize(640, 480))

        self.dialog: Optional[StartDialog] = None
        self.player = MediaPlayer(self)

        timer = QTimer(self)
        timer.timeout.connect(self.start_dialog)
        timer.start(10 * 1000)
        self.loop = loop or asyncio.get_event_loop()

        self.loop.run_until_complete(self.pass_context(periodic_update_schedule))

        self.loop.run_until_complete(self.pass_context(periodic_download_videos))

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.hide_stop()
        event.ignore()

    def hide_stop(self):
        self.player.stop()
        self.hide()
        self.window_opened = False

    def resizeEvent(self, event: QResizeEvent):
        self.player.resize(event.size().width(), event.size().height())

    def open_video(self, video_id):
        if not self.window_opened:
            self.close_dialog()
            self.window_opened = True
            self.showMaximized()
            self.player.showMaximized()
            self.player.new_video(video_path(video_id))

    def close_dialog(self):
        if self.dialog:
            self.dialog.hide()
        self.dialog_opened = False

    def start_dialog(self):
        if MainWindow.last_show_time:
            if datetime.now() - MainWindow.last_show_time < MainWindow.minimum_show_interval:
                return

        self.close_dialog()
        training = self.current_loop_training()
        if training and not self.window_opened and not self.dialog_opened:
            MainWindow.last_show_time = datetime.now()
            if not self.dialog:
                self.dialog = StartDialog()
            self.dialog.center()
            self.dialog_opened = True
            self.dialog.show()
            self.dialog.cancel_clicked.connect(self.close_dialog)
            self.dialog.start_clicked.connect(lambda: self.open_video(training.VideoID))

    async def pass_context(self, function):
        return await function(self)

    def current_loop_training(self) -> Optional[Training]:
        if self.schedule:
            current_time = datetime.now().strftime('%H:%M')
            day_of_week = datetime.now().weekday()
            trainings = self.schedule.get(day_of_week, [])
            if len(trainings) != 0:
                training: Optional[Training] = next(
                    iter(list(filter(lambda t: t.Time == current_time, trainings))), None)
                tr = Training()
                tr.VideoID = 6
                training = tr
                if training:
                    if Videos.downloaded_video.get(training.VideoID):
                        return training
                    print(f'no {training.VideoID} video')
                    Videos.download(training.VideoID)
        return None


def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow(loop)

    with loop:
        loop.run_forever()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
