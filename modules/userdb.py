import discord
import asyncio
import logging
from discord.ext import commands as broadsword
from config import config
from lib.db import DBMain

log = logging.getLogger(__name__)

class UserDB:
    """Store joined discord users in DB"""

    def __init__(self, bot):
        self.broadsword = bot
        
    async def on_member_join(self, member):
        try:
            log.info("User '{}' joined to the server.".format(member))
            self.cnx = DBMain()
            await self.cnx.discord_add_user(member.id)
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("cnx"):
                self.__dict__.pop(attr,None)

    async def on_member_remove(self, member):
        try:
            log.info("User '{}' left the server.".format(member))
            self.cnx = DBMain()
            await self.cnx.discord_delete_user(member.id)
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("cnx"):
                self.__dict__.pop(attr,None)

class TaskUserDB:
    def __init__(self, bot):
        self.broadsword = bot
        self._task = self.broadsword.loop.create_task(self.userdb_task())
        log.info("UserDB.Task should have been run.")
        
    def __unload(self):
        self._task.cancel()
        log.info("UserDB.Task should have been unloaded.")

    async def userdb_task(self):
        try:
            while not self.broadsword.is_closed:
                pass
                await asyncio.sleep(10)
        except Exception as e:
            print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.message_task())
        except asyncio.CancelledError:
            pass
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.userdb_task())
            
def setup(broadsword):
    broadsword.add_cog(UserDB(broadsword))
#    broadsword.add_cog(TaskUserDB(broadsword))
