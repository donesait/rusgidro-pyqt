import asyncio
import datetime
import json
import os
import sys
from typing import Optional, Dict, List, Coroutine

import requests
from PyQt6 import QtGui

from schedule import VideoSchedule
from pathlib import Path
from datetime import datetime

from qasync import QEventLoop, asyncSlot
from PyQt6.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal, pyqtSlot, QTimer, QSize
from PyQt6.QtGui import QResizeEvent, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow
from dotenv import load_dotenv

from constants import root_dir
from dto import Training
from start_dialog import StartDialog
from utils import resource_path, video_path, periodic, file_path
from video_player import MediaPlayer
from videos import Videos


@asyncSlot()
async def update_schedule(window):
    print('update schedule')
    schedule_task = window.loop.run_in_executor(None, VideoSchedule.update_data)
    await schedule_task
    window.schedule = VideoSchedule.dict_by_day


@asyncSlot()
async def download_videos(window):
    print('download_videos')
    download_task = window.loop.run_in_executor(None, Videos.download_all)
    await download_task
    window.downloaded_video = Videos.downloaded_video


@asyncSlot()
@periodic(5 * 60)
async def periodic_update_schedule(window):
    await update_schedule(window)


@asyncSlot()
@periodic(20 * 60)
async def periodic_download_videos(window):
    await download_videos(window)


class MainWindow(QMainWindow):
    def __init__(self, loop=None):
        super().__init__()

        videos_dir = resource_path('videos')
        if not os.path.exists(videos_dir):
            os.mkdir(videos_dir)

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

        self.loop.run_until_complete(self.pass_context(update_schedule))

        self.loop.run_until_complete(self.pass_context(download_videos))

    def closeEvent(self, event: QtGui.QCloseEvent):
        self.hide()
        self.window_opened = False
        event.ignore()

    def resizeEvent(self, event: QResizeEvent):
        self.player.resize(event.size().width(), event.size().height())

    def open_video(self, video_id):
        self.close_dialog()
        self.window_opened = True
        self.showMaximized()
        self.player.showMaximized()
        self.player.new_video(video_path(video_id))

    def close_dialog(self):
        if self.dialog:
            self.dialog.hide()

    def start_dialog(self):
        print('start_dialog')
        training = self.current_loop_training()
        if training and not self.window_opened and not self.dialog_opened:
            dialog = StartDialog(training.VideoID)
            dialog.center()
            self.dialog_opened = True
            dialog.show()
            dialog.rejected.connect(lambda: self.close_dialog)
            dialog.accepted.connect(lambda: self.open_video(training.VideoID))
        else:
            print('no training now or video plays')

    async def pass_context(self, function):
        return await function(self)

    def current_loop_training(self) -> Optional[Training]:
        if self.schedule:
            current_time = datetime.now().strftime('%H:%M')
            day_of_week = datetime.now().weekday()
            trainings = self.schedule.get(day_of_week, [])
            if len(trainings) != 0:
                training: Optional[Training] = next(
                    iter(list(filter(lambda t: t.DayOfWeek == current_time, trainings))), None)
                training = Training()
                training.VideoID = 6
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
