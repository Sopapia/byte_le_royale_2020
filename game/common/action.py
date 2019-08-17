from collections import deque

from game.config import *
from game.common.enums import *
from game.common.city import City
from game.common.disasters import *
from game.common.sensor import Sensor
from game.utils.helpers import enum_iter

class Action:
    def __init__(self):
        self._allocation_list = deque(maxlen=MAX_ALLOCATIONS_ALLOWED_PER_TURN)
        self._decree = None
        self.object_type = ObjectType.action

    def add_effort(self, action, amount):
        if not isinstance(amount, int) or not isinstance(amount, float):
            return
        if amount <= 0:
            return
        if action not in enum_iter(ActionType): 
            if not isinstance(action, Disaster) or not isinstance(action, Sensor):
                return
        self._allocation_list.append([action, int(amount)])

    def set_decree(self, dec):
        if dec not in enum_iter(PreemptiveType):
            return
        self._decree = dec

    def to_json(self):
        data = dict()
        json_allocation_list = deque(maxlen=MAX_ALLOCATIONS_ALLOWED_PER_TURN)
        for effort, number in self._allocation_list:
            if isinstance(effort, (City, Disaster, Sensor)):
                json_allocation_list.append([effort.to_json(), number])
            else:
                json_allocation_list.append([effort, number])
        data['effort'] = list(json_allocation_list)
        data['decree'] = self._decree
        data['object_type'] = self.object_type

        return data

    def from_json(self, data):
        self._allocation_list = deque(maxlen=MAX_ALLOCATIONS_ALLOWED_PER_TURN)
        for effort, number in data["effort"]:
            if isinstance(effort, dict) and "object_type" in effort:
                object_type = effort["object_type"]
                obj = None
                if object_type == ObjectType.city:
                    obj = City()
                    obj.from_json(effort)
                elif object_type == ObjectType.disaster:
                    dis_type = effort['type']
                    if dis_type == DisasterType.earthquake:
                        obj = Earthquake()
                    elif dis_type == DisasterType.fire:
                        obj = Fire()
                    elif dis_type == DisasterType.hurricane:
                        obj = Hurricane()
                    elif dis_type == DisasterType.monster:
                        obj = Monster()
                    elif dis_type == DisasterType.tornado:
                        obj = Tornado()
                    elif dis_type == DisasterType.ufo:
                        obj = Ufo()
                    obj.from_json(effort)
                elif object_type == ObjectType.sensor:
                    obj = Sensor()
                    obj.from_json(effort)
                self._allocation_list.append([obj, number])
            else:
                self._allocation_list.append([effort, number])
        self._decree = data["decree"]
        self.object_type = data["object_type"]
