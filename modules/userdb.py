import discord
import asyncio
import logging
from discord.ext import commands as broadsword
from config import config
from lib.libdb import DBMain

log = logging.getLogger(__name__)

class UserDB:
    """Store joined discord users in DB"""

    def __init__(self, bot):
        self.broadsword = bot

    async def on_member_join(self, member):
        try:
            print("User {} joined".format(member))
            self.cnx = DBMain()
            await self.cnx.discord_add_user(member.id)
        except Exception as e:
            print(e)
        finally:
            for attr in ("cnx"):
                self.__dict__.pop(attr,None)

    async def on_member_remove(self, member):
        try:
            print("User {} left".format(member))
            self.cnx = DBMain()
            await self.cnx.discord_delete_user(member.id)
        except Exception as e:
            print(e)
        finally:
            for attr in ("cnx"):
                self.__dict__.pop(attr,None)

class TaskUserDB:
    def __init__(self, bot):
        self.broadsword = bot
        self._task = self.broadsword.loop.create_task(self.taskUserDB())
        print('QueueMessages.taskGC should have been run..')
        
    def __unload(self):
        self._task.cancel()
        print('QueueMessages.taskGC should have been unloaded..')

    async def taskUserDB(self):
        try:
            while not self.broadsword.is_closed:
                pass
                await asyncio.sleep(60)
        except asyncio.CancelledError as e:
            print(e)
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.taskUserDB())
            
def setup(broadsword):
    broadsword.add_cog(UserDB(broadsword))
#    broadsword.add_cog(TaskUserDB(broadsword))
