import os
from typing import Dict

from api import Api
from utils import video_path


class Videos:
    downloaded_video: Dict[int, bool] = {}

    @staticmethod
    def download_all():
        print('download_all')
        videos = Api.get_videos()
        for video in videos:
            if not os.path.exists(video_path(video.ID)):
                Api.download(f'{video.ID}.mp4')
            Videos.downloaded_video[video.ID] = True

    @staticmethod
    def download(video_id: int):
        Api.download(f'{video_id}.mp4')
        Videos.downloaded_video[video_id] = True
