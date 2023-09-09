from enum import Enum
from typing import Optional, List


class Dto:
    def to_json(self):
        pass


def json_list(obj_list: List[Dto]):
    result = []
    for obj in obj_list:
        result.append(obj.to_json())


class Training(Dto):
    def __init__(self):
        self.ID: int = 0
        self.CreatedAt: str = ''
        self.UpdatedAt: str = ''
        self.DeletedAt: Optional[str] = None
        self.DayOfWeek: int = -1
        self.Time: str = ''
        self.VideoID: int = 0

    def to_json(self):
        return {
            'ID': self.ID,
            'CreatedAt': self.CreatedAt,
            'UpdatedAt': self.UpdatedAt,
            'DeletedAt': self.DeletedAt,
            'DayOfWeek': self.DayOfWeek,
            'Time': self.Time,
            'VideoID': self.VideoID,
        }


class Video(Dto):
    def __init__(self):
        self.ID: int = 0
        self.CreatedAt: str = ''
        self.UpdatedAt: str = ''
        self.DeletedAt: Optional[str] = None
        self.Name = ''
        self.Archived: bool = False

    def to_json(self):
        return {
            'ID': self.ID,
            'CreatedAt': self.CreatedAt,
            'UpdatedAt': self.UpdatedAt,
            'DeletedAt': self.DeletedAt,
            'Name': self.Name,
            'Archived': self.Archived
        }


class StatType(str, Enum):
    decline = 'decline'
    half = 'half'
    full = 'full'
