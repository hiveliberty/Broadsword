import asyncio
import datetime
import discord
import logging
from discord.ext import commands as broadsword

from config import config

log = logging.getLogger(__name__)

class CleanUp:
    def __init__(self, bot):
        self.broadsword = bot
        self.msg_start = ("{} should have been run."
                          .format(__class__.__name__))
        self.msg_stop = ("{} should have been unloaded."
                         .format(__class__.__name__))
        self.channels = config.bot["cleanupchannels"]
        self.log_channel = self.broadsword.get_channel(config.bot["log_channel"])
        log.info("CleanUp.Task log channel is {}.".format(self.log_channel))
        self._task = self.broadsword.loop.create_task(self.cleanup_task())
        log.info(self.msg_start)

    def __unload(self):
        self._task.cancel()
        log.info(self.msg_stop)

    async def cleanup_task(self):
        try:
            while not self.broadsword.is_closed:
                utc = datetime.datetime.utcnow()
                offset = datetime.timedelta(hours = 12)
                before = utc - offset
                # log.info("UTC Time: {} | Offset Time: {}".format(utc,before))
                for id in self.channels:
                    channel = self.broadsword.get_channel(id)
                    if channel is not None:
                        log.info("CleanUp: try purge old messages"
                                 " from channel '{}'.".format(channel))
                        await self.broadsword.purge_from(
                            channel, limit = 99, before = before)
                del utc,before
                await asyncio.sleep(60)
        except asyncio.CancelledError:
            pass
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.cleanup_task())
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.cleanup_task())


def setup(broadsword):
    broadsword.add_cog(CleanUp(broadsword))