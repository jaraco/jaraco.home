import sys
from typing import TYPE_CHECKING

if sys.platform != "darwin" and TYPE_CHECKING:
    assert False  # https://github.com/python/mypy/issues/9025#issuecomment-1087270212

import asyncio
import pathlib
import subprocess

import keyring
import typer
import victor_smart_kill as vsk

from . import contact
from .compat.py38 import resources

app = typer.Typer()


async def check_traps():
    username = contact.load().email
    password = keyring.get_password('https://www.victorpest.com', username)
    async with vsk.VictorAsyncClient(username, password) as client:
        api = vsk.VictorApi(client)
        traps = await api.get_traps()
        return any(trap.status for trap in traps)


class TrapWatch:
    def __init__(self):
        self.app = rumps.App("Traps", icon=self.icon)
        rumps.Timer(self.check_traps, 3600).start()
        self.app.run()

    def check_traps(self, timer):
        if asyncio.run(check_traps()):
            rumps.notification(
                "Smart Traps",
                subtitle=None,
                message="Check the traps.",
                img=self.icon,
            )

    @property
    def icon(self):
        return str(resources.files() / 'mouse.png')


@app.command()
def install():
    name = 'Trap Watcher.plist'
    agents = pathlib.Path('~/Library/LaunchAgents').expanduser()
    target = agents / name
    tmpl = resources.files().joinpath(name).read_text()
    logs = pathlib.Path(sys.executable).parent.parent / 'logs'
    source = tmpl.format(sys=sys, logs=logs)
    target.write_text(source)
    subprocess.check_output(['launchctl', 'load', target])


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, update: bool = False):
    if ctx.invoked_subcommand:
        return
    TrapWatch()


if __name__ == '__main__':
    # This check and import must be delayed as to not break pytest discovery
    if sys.platform != "darwin":
        print("This app is only available on MacOS.")
        sys.exit(1)

    import rumps

    app()
