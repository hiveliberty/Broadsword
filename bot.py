import os
import asyncio
import gc
from discord.ext import commands
from config import config
from lib.utils import BasicUtils
from lib.libdb import DBStart
#from lib.libdb import DB

gc.enable()

main_modules = {
    "modules.admin",
#    "modules.queues",
#    "modules.userdb",
}

def main():

    try:
        cnx = DBStart()
        mysql_version = cnx.mysql_version()
        stored_db_version = cnx.get_key("db_version")
        db_version = BasicUtils.db_version()
        if stored_db_version is None:
            cnx.set_key("db_version", db_version)
            stored_db_version = db_version
        else:
            if stored_db_version["storedValue"] < db_version:
                print("Database update required")
    except Exception as e:
        print(e)
        print("MySQL DB is not available! BroadswordBot will not be started!")
        return None
    finally:
        del cnx
    
    try:
        cnx = DBStart()
        cnx.check_message_queue()
    except Exception as e:
        print(e)
    finally:
        del cnx

    local_ver = BasicUtils.bot_version()
    remote _ver = BasicUtils.load_version()
    if ver < "0.2.0":
        print(mver)
        print("Bot update required!")
        return

    print('Connecting...')

    broadsword = commands.Bot(command_prefix=config.bot["prefix"])

    @broadsword.event
    async def on_ready():
        """A function that is called when the client is
        done preparing data received from Discord.
        """

        print('Broadsword is logged in')
        print('Username: {}'.format(broadsword.user.name))
        print('User ID: {}'.format(broadsword.user.id))
        print('Version v.{}'.format(BasicUtils.bot_version()))
        print('MySQL v.{}'.format(mysql_version))
        print('DB v.{}'.format(stored_db_version["storedValue"]))
        print('-----------------------')

        #   Load main modules
        for main_module in main_modules:
            try:
                broadsword.load_extension(main_module)
                print("{} loaded.".format(main_module))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(main_module, exc))
                return

        #   Load user modules
        for plugin, options in config.plugins.items():
            if not options.get('enabled', True):
                continue
            try:
                broadsword.load_extension(plugin)
                print("{} loaded.".format(plugin))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(plugin, exc))
                return

    broadsword.run(config.bot["token"])
    broadsword.loop.close()
    broadsword.logout()
    print('-----------------------')
    print('Connection closed.')

if __name__ == '__main__':
    main()