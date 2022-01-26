from datetime import datetime
from functools import wraps

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