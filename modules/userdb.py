import gc
from discord.ext import commands as broadsword
from importlib import reload
from config import config

class UserDB:
    """Store joined discord users in DB"""

    def __init__(self, bot):
        self.broadsword = bot

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