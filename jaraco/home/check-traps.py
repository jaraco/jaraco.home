import autocommand
import keyring
import victor_smart_kill as vsk

from . import contact


@autocommand.autocommand(__name__, loop=True)
async def check_traps():
    username = contact.load().email
    password = keyring.get_password('https://www.victorpest.com', username)
    async with vsk.VictorAsyncClient(username, password) as client:
        api = vsk.VictorApi(client)
        traps = await api.get_traps()
        for trap in traps:
            if trap.trapstatistics.kills_present:
                print(trap.name, "needs attention")
        return any(trap.status for trap in traps)
