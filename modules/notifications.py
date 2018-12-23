import sys
import time
import yaml
import datetime
import asyncio
import discord
import logging
from discord.ext import commands as broadsword
#import xmltodict

from lib.utils import EVEUtils
from lib.db import DBMain
from lib.token import EVEToken
from lib.esi import ESIApi
from lib.notifications import NotifFormatter
from config import config

log = logging.getLogger(__name__)

class EVENotifications:
    def __init__(self, bot):
        self.broadsword = bot
        self.task_interval = 30
        self.interval = config.notifications["check_interval"]
        self.channel = config.notifications["channel_id"]
        self._task = self.broadsword.loop.create_task(self._run_task())
        self.msg_start = "{} should have been run.".\
            format(__class__.__name__)
        self.msg_stop = "{} should have been unloaded.".\
            format(__class__.__name__)
        log.info(self.msg_start)

    def __unload(self):
        self._task.cancel()
        log.info(self.msg_stop)

    async def _run_task(self):
        try:
            while not self.broadsword.is_closed:
                cnx = DBMain()
                time_next = await cnx.custom_get("nextNotifCheck")
                if config.bot["devMode"]:
                    log.info("Next check: {}".format(time_next))

                if time_next is not None:
                    time_next = datetime.datetime.fromtimestamp(float(time_next))
                    if self.now() >= time_next:
                        log.info("Start periodic check corp\\alliance notifications.")
                        await self._check()
                else:
                    await cnx.custom_add("nextNotifCheck", await self.next_check(self.interval))
                del cnx
                for attr in ("cnx", "t_next", "t_now"):
                    self.__dict__.pop(attr,None)
                await asyncio.sleep(self.task_interval)
        except asyncio.CancelledError:
            pass
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self._run_task())
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self._run_task())

    async def _check(self):
        try:
            self.cnx = DBMain()
            latestNotifID = int(await self.cnx.custom_get("latestNotifID"))
            member_id = int(await self.cnx.custom_get("member_id"))
            if latestNotifID is None:
                latestNotifID = 0
                await self.cnx.custom_add("latestNotifID", latestNotifID)
            oldlatestNotifID = latestNotifID

            if config.bot["devMode"]:
                log.info("latestNotifID: {}".format(latestNotifID))
                log.info("latestNotifID (int): {}".format(int(latestNotifID)))

            esiclient = ESIApi()
            token_api = EVEToken()
            token = await token_api.get_token(
                "notifications_token", "esi-characters.read_notifications.v1")

            notifications = await esiclient.notifications_get(
                token["character_id"], token["access_token"])

            for notification in notifications:
                if notification["notification_id"] > latestNotifID:
                    # if notification["sender_id"] != member_id:
                        # pass
                    latestNotifID = notification["notification_id"]
                    if notification["type"] in config.notifications["whitelist"]:
                        await self._send(notification)

            if latestNotifID > oldlatestNotifID:
                await self.cnx.custom_update("latestNotifID", latestNotifID)
            await self.cnx.custom_update("nextNotifCheck", self.next_check(self.interval))
            del self.cnx
            return
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def _send(self, data):
        try:
            if config.bot["devMode"]:
                log.info("Notification Data: {}".format(data))
            formatter = NotifFormatter(data)
            text = await formatter.get_formatted()
            msg = "@everyone, __attention!__ \n\n"
            msg += "**--------------------------**\n"
            msg += "**Date: **{}\n".format(
                await EVEUtils.timestamp_to_date(data["timestamp"]))
            msg += "{}\n".format(text)
            msg += "\n**----------------------------**\n"
            await self.cnx.message_add(msg, self.channel)
            return
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    def next_check(self, interval):
        t_next = self.now() + datetime.timedelta(seconds=interval)
        t_next = time.mktime(t_next.timetuple())
        return t_next

    def now(self):
        t_now = datetime.datetime.now().replace(microsecond=0)
        return t_now

def setup(broadsword):
    broadsword.add_cog(EVENotifications(broadsword))
