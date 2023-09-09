import asyncio
import os
import sys
from typing import TypeVar, Type, List

from constants import root_dir


def periodic(period):
    def scheduler(func):
        async def wrapper(*args, **kwargs):
            while True:
                asyncio.create_task(func(*args, **kwargs))
                await asyncio.sleep(period)

        return wrapper

    return scheduler


# Define function to import external files when using PyInstaller.
def resource_path(*relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *relative_path)


T = TypeVar('T', bound=object)


def object_from_dict(obj_type: Type[T], data: dict) -> T:
    obj = obj_type()
    for key, value in data.items():
        if hasattr(obj, key):
            setattr(obj, key, value)
    return obj


def list_of_objects_from_list(obj_type: Type[T], data: List[dict]) -> List[T]:
    result: List[T] = []
    for dict_element in data:
        obj = object_from_dict(obj_type, dict_element)
        result.append(obj)
    return result


def video_path(video_id):
    return file_path(f'{video_id}.mp4')


def file_path(filename):
    return os.path.join(root_dir, 'videos', filename)
