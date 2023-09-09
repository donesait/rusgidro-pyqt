import json
import os
from typing import List, Dict

from api import Api
from constants import root_dir
from dto import Training, json_list


class VideoSchedule:
    _schedule_path = os.path.join(root_dir, 'schedule.json')
    is_empty = True
    dict_by_day: Dict[int, List[Training]] = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }

    @staticmethod
    def update_data():
        try:
            trainings = Api.get_schedule()
        except Exception:
            trainings = []

        if len(trainings) == 0:
            with open(VideoSchedule._schedule_path) as file:
                VideoSchedule.dict_by_day.update(json.load(file))
            VideoSchedule.is_empty = False
        else:
            for training in trainings:
                if training.DayOfWeek in VideoSchedule.dict_by_day:
                    VideoSchedule.dict_by_day[training.DayOfWeek].append(training)
            VideoSchedule.is_empty = False
            with open(VideoSchedule._schedule_path, 'w') as file:
                dict_to_write = {}
                for day, trainings in VideoSchedule.dict_by_day.items():
                    dict_to_write[day] = json_list(trainings)

                json.dump(dict_to_write, file)
