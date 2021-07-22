import functools
import contextlib
import time
import subprocess
from jaraco.functools import retry


def parse_field(item):
    key, value = item.split('=')
    with contextlib.suppress(ValueError):
        value = int(value)
    if value == 'none':
        value = None
    return value


def parse_status(line):
    return dict(map(parse_field, line.split()))


sleep_2 = functools.partial(time.sleep, 2)


@retry(retries=2, cleanup=sleep_2, trap=Exception)
def get_status(tuner_id):
    cmd = ['hdhomerun_config', 'FFFFFFFF', 'get', f'/tuner{tuner_id}/status']
    line = subprocess.check_output(cmd)
    return parse_status(line)


def set_channel(tuner_id, channel):
    channel_str = str(channel) if channel else 'none'
    cmd = [
        'hdhomerun_config', 'FFFFFFFF', 'set',
        f'/tuner{tuner_id}/channel', channel_str]
    line = subprocess.check_output(cmd)
    return parse_status(line)


def find_idle_tuner():
    for id in range(4):
        status = get_status(id)
        if not status['ch']:
            return id


def gather_status():
    tuner = find_idle_tuner()

    for channel in 34, 35, 36:
        set_channel(tuner, channel)
        yield get_status(tuner)
    set_channel(tuner, None)


def run():
    for status in gather_status():
        print(status)


__name__ == '__main__' and run()
