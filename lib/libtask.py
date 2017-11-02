#==============================================================================
#
#   Bot background tasks
#
#==============================================================================

import asyncio
#from discord.ext import commands as broadsword
from lib.libdb import DB
from config import config

#==============================================================================

class BotTasks:
    async def sendQueueMessage(self, broadsword):
        while not broadsword.is_closed:
            self.cnx = DB()
            self.x = 0
            while self.x < 3:
                self.id = self.cnx.gelOldestQueueMessage()
                self.id = self.id['MIN(id)']
                if self.id is None:
                    self.id = 1
                self.queued_msg = await self.cnx.getQueuedMessage(self.id)
                if self.queued_msg is not None:
                    if self.queued_msg['channel'] is None:
                        await self.cnx.delQueuedMessage(self.id)
                    await broadsword.send_message(discord.Object(id=self.queued_msg['channel']), self.queued_msg['message'])
                self.x += 1
            await asyncio.sleep(7)

    async def testTask(self, broadsword):
        while not broadsword.is_closed:
            self.x = 0
            while self.x < 3:
                await broadsword.send_message(discord.Object(id='362284304497115146'), self.x)
                self.x += 1
            await asyncio.sleep(7)