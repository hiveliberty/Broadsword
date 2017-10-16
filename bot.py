VERSION = "0.3.2.b03"

from discord.ext import commands
from config import config
import os

modules = config.plugins2

print('Connecting...')
broadsword = commands.Bot(command_prefix=config.bot["prefix"])

def main():
    @broadsword.event
    async def on_ready():
        """A function that is called when the client is
        done preparing data received from Discord.
        """

        print('Broadsword is logged in')
        print('Username: {}'.format(broadsword.user.name))
        print('User ID: {}'.format(broadsword.user.id))
        print('Version v.' + VERSION)
        print('-----------------------')

        for module, options in modules.items():
            if not options.get('enabled', True):
                continue
            try:
                broadsword.load_extension(module)
                print("{} loaded.".format(module))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(module, exc))

    broadsword.run(config.bot["token"])
    broadsword.loop.close()
    print('-----------------------')
    print('Connection closed.')

if __name__ == '__main__':
    main()