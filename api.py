import getpass
import json
import os
from typing import List, Type

import requests
from dotenv import load_dotenv

from dto import Training, Video, StatType
from utils import list_of_objects_from_list, file_path

load_dotenv()
api_url = os.getenv("API_URL")


class Api:
    @staticmethod
    def get_schedule() -> List[Training]:
        response = requests.get(f'{api_url}/api/v1/schedule')
        if response.status_code != 200:
            return []
        data = json.loads(response.content)
        result = list_of_objects_from_list(Training, data)
        return result

    @staticmethod
    def get_videos() -> List[Video]:
        response = requests.get(f'{api_url}/api/v1/videos')
        if response.status_code != 200:
            return []
        data = json.loads(response.content)
        result = list_of_objects_from_list(Video, data)
        return result

    @staticmethod
    def download(filename: str):
        response = requests.get(f'{api_url}/upload/{filename}')
        open(file_path(filename), 'wb').write(response.content)

    @staticmethod
    def send_stat(video_id: int, stat_type: StatType):
        data = {
            'Name': getpass.getuser(),
            'VID': video_id,
            'Type': stat_type
        }
        requests.post(f'{api_url}/api/v1/stats', data)
