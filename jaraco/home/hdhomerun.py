import functools
import contextlib
import time
import subprocess
import sys
import pathlib
from importlib.resources import files

import keyring
from jaraco.functools import retry
from jaraco.mongodb.helper import connect_db


def parse_field(item):
    key, value = item.split('=')
    with contextlib.suppress(ValueError):
        value = int(value)
    if value == 'none':
        value = None
    return key, value


def parse_status(line):
    return dict(map(parse_field, line.split()))


sleep_2 = functools.partial(time.sleep, 2)


hdhomerun_config = '/usr/local/bin/hdhomerun_config'


@retry(retries=5, cleanup=sleep_2, trap=Exception)
def get_status(tuner_id):
    cmd = [hdhomerun_config, 'FFFFFFFF', 'get', f'/tuner{tuner_id}/status']
    line = subprocess.check_output(cmd, text=True)
    return parse_status(line)


@retry(retries=5, cleanup=sleep_2, trap=Exception)
def set_channel(tuner_id, channel):
    channel_str = str(channel) if channel else 'none'
    cmd = [
        hdhomerun_config,
        'FFFFFFFF',
        'set',
        f'/tuner{tuner_id}/channel',
        channel_str,
    ]
    subprocess.check_call(cmd)


def find_idle_tuner():
    for id in range(4):
        status = get_status(id)
        if not status['ch']:
            return id
    raise RuntimeError("Could not find idle tuner")


def gather_status():
    tuner = find_idle_tuner()

    for channel in 34, 35, 36:
        set_channel(tuner, channel)
        yield get_status(tuner)
    set_channel(tuner, None)


def install():
    name = 'Gather HDHomeRun Stats.plist'
    agents = pathlib.Path('~/Library/LaunchAgents').expanduser()
    target = agents / name
    tmpl_name = files(__package__) / name
    tmpl = tmpl_name.read_text()
    logs = pathlib.Path(sys.executable).parent.parent / 'logs'
    source = tmpl.format(sys=sys, logs=logs)
    target.write_text(source)
    subprocess.check_output(['launchctl', 'load', target])


def inject_creds(url):
    username = 'jaraco'
    password = keyring.get_password(url, username)
    assert password, "No password found"
    return url.replace('://', f'://{username}:{password}@')


def run():
    url = 'mongodb+srv://cluster0.x8wjx.mongodb.net/hdhomerun'
    db = connect_db(inject_creds(url))
    with contextlib.suppress(Exception):
        db.create_collection('statuses', capped=True, size=102400)
    db.statuses.insert_many(gather_status())


def update():
    cmd = [
        sys.executable,
        '-m',
        'pip',
        'install',
        '--quiet',
        '--upgrade',
        '--upgrade-strategy',
        'eager',
        'jaraco.home',
    ]
    subprocess.run(cmd)


def main():
    if 'install' in sys.argv:
        return install()
    run()
    if '--update' in sys.argv:
        update()


__name__ == '__main__' and main()
