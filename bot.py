import os
import asyncio
from discord.ext import commands
from config import config
from lib import utils
from lib.libdb import DBStart
from lib.libdb import DB

def main():
    cnx = DBStart()
    try:
        dbversion = cnx.version()
    except:
        print("MySQL DB is not available! BroadswordBot will not be started!")
        return None
    cnx.checkMessageQueue()
    del cnx

    print('Connecting...')

    plugins = config.plugins

    broadsword = commands.Bot(command_prefix=config.bot["prefix"])

    @broadsword.event
    async def on_ready():
        """A function that is called when the client is
        done preparing data received from Discord.
        """

        print('Broadsword is logged in')
        print('Username: {}'.format(broadsword.user.name))
        print('User ID: {}'.format(broadsword.user.id))
        print('Version v.{}'.format(utils.getVersion()))
        print('MySQL v.{}'.format(dbversion))
        print('-----------------------')

        for plugin, options in plugins.items():
            if not options.get('enabled', True):
                continue
            try:
                broadsword.load_extension(plugin)
                print("{} loaded.".format(plugin))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(plugin, exc))

    broadsword.run(config.bot["token"])
    broadsword.loop.close()
    print('-----------------------')
    print('Connection closed.')

if __name__ == '__main__':
    main()