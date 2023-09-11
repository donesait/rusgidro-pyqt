import os
from typing import Dict

from api import Api
from constants import root_dir
from utils import video_path


class Videos:
    downloaded_video: Dict[int, bool] = {}

    @staticmethod
    def check_videos():
        for filename in os.listdir(os.path.join(root_dir, 'videos')):
            try:
                name, extension = filename.split('.')
                if extension == 'mp4':
                    try:
                        Videos.downloaded_video[int(name)] = True
                    except ValueError:
                        ...
            except ValueError:
                ...

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
