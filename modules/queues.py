#import urllib.parse as urllib
import discord
import asyncio
import logging
from discord.ext import commands as broadsword
from config import config
from lib.db import DBMain

log = logging.getLogger(__name__)


class QueueMessages:
    def __init__(self, bot):
        self.broadsword = bot
        self._task = self.broadsword.loop.create_task(self.message_task())
        self.msg_start = "{} should have been run.".\
            format(__class__.__name__)
        self.msg_stop = "{} should have been unloaded.".\
            format(__class__.__name__)
        log.info(self.msg_start)

    def __unload(self):
        self._task.cancel()
        log.info(self.msg_stop)

    async def message_task(self):
        try:
            while not self.broadsword.is_closed:
                self.cnx = DBMain()
                self.x = 0
                while self.x < 3:
                    self.id = await self.cnx.message_get_oldest()
                    if self.id is None:
                        break
                    self.queued_msg = await self.cnx.message_get(self.id)
                    if self.queued_msg is not None:
                        if self.queued_msg['channel_id'] is None:
                            await self.cnx.message_delete(self.id)
                            continue
                        if self.queued_msg['message'] is None:
                            await self.cnx.message_delete(self.id)
                            continue
                        self.channel = self.broadsword.get_channel(self.queued_msg['channel_id'])
                        await self.broadsword.send_message(self.channel, self.queued_msg['message'])
                        await self.cnx.message_delete(self.id)
                    else:
                        continue
                    self.x += 1
                    for attr in ("channel", "queued_msg", "id"):
                        self.__dict__.pop(attr,None)
                del self.cnx
                await asyncio.sleep(7)
        except asyncio.CancelledError:
            pass
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.message_task())
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.message_task())


class QueueRename:
    def __init__(self, bot):
        self.broadsword = bot
        self._task = self.broadsword.loop.create_task(self.rename_task())
        self.msg_start = "{} should have been run.".\
            format(__class__.__name__)
        self.msg_stop = "{} should have been unloaded.".\
            format(__class__.__name__)
        log.info(self.msg_start)

    def __unload(self):
        self._task.cancel()
        log.info(self.msg_stop)

    async def rename_task(self):
        try:
            while not self.broadsword.is_closed:
                self.server = self.broadsword.get_server(id=config.bot['guild'])
                self.cnx = DBMain()
                self.x = 0
                while self.x < 4:
                    self.id = await self.cnx.rename_get_oldest()
                    if self.id is None:
                        break
                    self.queued_rename = await self.cnx.rename_get(self.id)
                    if self.queued_rename is not None:
                        if self.queued_rename['discord_id'] is None:
                            await self.cnx.rename_delete(self.id)
                            continue
                        if self.queued_rename['nick'] is None:
                            await self.cnx.rename_delete(self.id)
                            continue
                        try:
                            self.member = self.server.get_member(self.queued_rename['discord_id'])
                            await self.broadsword.change_nickname(self.member, self.queued_rename['nick'])
                            await self.cnx.rename_delete(self.id)
                        except discord.Forbidden as e:
                            if self.queued_rename['discord_id'] == self.server.owner.id:
                                log.info("Owner cann't be renamed!")
                                await self.cnx.rename_delete(self.id)
                                continue
                            if e.text == "Privilege is too low...":
                                log.info("BroadswordBot needs more privileges for rename members!")
                                continue
                    else:
                        continue
                    self.x += 1
                    for attr in ("member", "queued_rename", "id"):
                        self.__dict__.pop(attr,None)
                del self.cnx
                await asyncio.sleep(10)
        except asyncio.CancelledError:
            pass
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.rename_task())
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.rename_task())

def setup(broadsword):
    broadsword.add_cog(QueueMessages(broadsword))
    broadsword.add_cog(QueueRename(broadsword))
