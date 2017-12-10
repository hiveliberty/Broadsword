import os
import asyncio
import gc
from datetime import datetime
from discord.ext import commands
from config import config
from lib.utils import BasicUtils
from lib.libdb import DBStart

gc.enable() # Not sure that this working..

main_modules = {
    "modules.admin",
    "modules.test",
    "modules.queues",
    "modules.userdb",
}

def main():

    try:
        cnx = DBStart()
        mysql_version = cnx.mysql_version()
        #stored_db_version = cnx.storage_get("db_version")
        #db_version = BasicUtils.db_version()
        #if stored_db_version is None:
        #    cnx.storage_add("db_version", db_version)
        #    stored_db_version = db_version
        #else:
            # There should be an update of the database
        #    if stored_db_version["storedValue"] < db_version:
        #        print("Database update required")
        #        return
    except Exception as e:
        print(e)
        print("MySQL DB is not available! BroadswordBot will not be started!")
        return
    finally:
        del cnx
    
    try:
        cnx = DBStart()
        cnx.message_check()
    except Exception as e:
        print(e)
    finally:
        del cnx
    
    # If enabled in config, prevent the bot from running until it is updated
    if config.bot["checkUpdates"]:
        if BasicUtils.check_update() is None:
            print("Cann't check new version!")
        else:
            if BasicUtils.check_update():
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
        #print('DB v.{}'.format(stored_db_version["storedValue"]))
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
