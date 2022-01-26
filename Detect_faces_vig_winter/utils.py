from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from typing import Dict

__measure_time_enabled: bool = False


def enable_measure_time():
    global __measure_time_enabled
    __measure_time_enabled = True


def disable_measure_time():
    global __measure_time_enabled
    __measure_time_enabled = False


def measure_time(method):

    @wraps(method)
    def _impl(self, *args, **kwargs):
        call = lambda: method(self, *args, **kwargs)

        if not __measure_time_enabled:
            return call()

        name = method.__name__

        start = datetime.now()

        print(f'[{name} start]')

        result = call()

        end = datetime.now()

        print(f'[{name} end] {end - start}')

        return result

    return _impl


@dataclass(frozen=True)
class BoundingBox:
    height: float
    width: float
    top: float
    left: float

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top - self.height

    def parse(data: Dict):

        return BoundingBox(
            height=data['Height'],
            width=data['Width'],
            top=data['Top'],
            left=data['Left'],
        )