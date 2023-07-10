import datetime
import json
import os
import sys
import requests
from pathlib import Path
from datetime import datetime

from PyQt6.QtCore import QRunnable, QThreadPool, QObject, pyqtSignal, pyqtSlot, QTimer, QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow
from dotenv import load_dotenv

from constants import ROOT_DIR
from start_dialog import StartDialog
from video_player import MediaPlayer

load_dotenv()
api_url = os.getenv("API_URL")

schedule = {}


def video_path(video_id):
    return f'{ROOT_DIR}/videos/{video_id}.mp4'


class WorkerSignals(QObject):
    result = pyqtSignal(str)


# class DownloadWorker(QRunnable):
#     def __init__(self):
#         super().__init__()
#
#     @pyqtSlot()
#     def run(self):
#         print("DownloadWorker launched")
#         videos_response = requests.get(f'{api_url}/api/v1/videos')
#         videos = json.loads(videos_response.content)
#         for video in videos:
#             Path(f'{ROOT_DIR}/videos').mkdir(exist_ok=True)
#             filename = f'{video["ID"]}.mp4'
#             if not os.path.exists(video_path(video["ID"])):
#                 response = requests.get(f'{api_url}/upload/{filename}')
#                 open(video_path(video["ID"]), 'wb').write(response.content)


class VideoIdSignals(QObject):
    video_signal = pyqtSignal(int)


class VideoWorker(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = VideoIdSignals()

    @pyqtSlot()
    def run(self):
        print("VideoWorker launched")
        now = datetime.now()
        for training in schedule.get(now.weekday(), []):
            # if training['Time'] == now.strftime('%H:%M'):
            if True:
                self.signals.video_signal.emit(training['VideoID'])


# class ScheduleWorker(QRunnable):
#     def __init__(self):
#         super().__init__()
#
#     @pyqtSlot()
#     def run(self):
#         print("ScheduleWorker launched")
#         weekday = datetime.now().weekday()
#         response = requests.get(f'{api_url}/api/v1/schedule/{weekday}')
#         schedule_path = f'{ROOT_DIR}/schedule.json'
#         if response.status_code == 200:
#             schedule[weekday] = json.loads(response.content)
#             with open(schedule_path, 'w') as file:
#                 json.dump(schedule, file)
#         else:
#             with open(schedule_path) as file:
#                 schedule.update(json.load(file))


class ProcessRunnable(QRunnable):
    def __init__(self, target, args):
        super().__init__()
        self.t = target
        self.args = args

    def run(self):
        self.t(*self.args)

    def start(self):
        QThreadPool.globalInstance().start(self)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.threadpool = QThreadPool()

        self.player = MediaPlayer()

        self.download_videos()
        self.check_schedule()
        # self.check_time()

    def start_dialog(self, video_id):
        print('start_dialog\n')
        dialog = StartDialog(video_id)
        dialog.start_clicked.connect(lambda: self.start_video(video_id))
        dialog.cancel_clicked.connect(lambda: dialog.close())

    def start_video(self, video_id):
        print('start_video\n')
        self.player.new_video(video_path(video_id))
        self.player.showMaximized()

    def check_schedule(self):
        weekday = datetime.now().weekday()
        response = requests.get(f'{api_url}/api/v1/schedule/{weekday}')
        schedule_path = f'{ROOT_DIR}/schedule.json'
        if response.status_code == 200:
            schedule[weekday] = json.loads(response.content)
            with open(schedule_path, 'w') as file:
                json.dump(schedule, file)
        else:
            with open(schedule_path) as file:
                schedule.update(json.load(file))

    def download_videos(self):
        videos_response = requests.get(f'{api_url}/api/v1/videos')
        videos = json.loads(videos_response.content)
        for video in videos:
            Path(f'{ROOT_DIR}/videos').mkdir(exist_ok=True)
            filename = f'{video["ID"]}.mp4'
            if not os.path.exists(video_path(video["ID"])):
                response = requests.get(f'{api_url}/upload/{filename}')
                open(video_path(video["ID"]), 'wb').write(response.content)

    # def check_time(self):
    #     worker = VideoWorker()
    #     worker.signals.video_signal.connect(self.start_dialog)
    #     self.threadpool.start(worker)
    #     QTimer.singleShot(30 * 1000, self.check_time)
    #
    # def check_schedule(self):
    #     worker = ScheduleWorker()
    #     self.threadpool.start(worker)
    #     QTimer.singleShot(60 * 60 * 1000, self.check_schedule)
    #
    # def download_video(self):
    #     worker = DownloadWorker()
    #     self.threadpool.start(worker)
    #     QTimer.singleShot(30 * 60 * 1000, self.check_time)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    app.exec()
