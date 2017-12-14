import sys
import time
import datetime
import asyncio
import discord
import logging
from discord.ext import commands as broadsword
#import xmltodict
from lib.utils import MailUtils
from lib.db import DBMain
from lib.eve import EVEBasic
from config import config

log = logging.getLogger(__name__)

class EVEMail:
    def __init__(self, bot):
        self.broadsword = bot
        #self.server = self.broadsword.get_server(id=config.bot["guild"])
        self.interval = 10
        self.channel = config.evemails["channelID"]
        self._task = self.broadsword.loop.create_task(self.mail_task())
        print('MailTask should have been run in background..')
        
    def __unload(self):
        self._task.cancel()
        print('MailTask should have been unloaded..')
        
    async def mail_task(self):
        try:
            while not self.broadsword.is_closed:
                self.cnx = DBMain()
                self.time_next = await self.cnx.storage_get("nextMailCheck")

                if self.time_next is not None:
                    self.time_next = datetime.datetime.fromtimestamp(float(self.time_next))
                    self.time_now = datetime.datetime.now().replace(microsecond=0)

                    print("{0} <= {1}".format(self.time_next, self.time_now))
                    if self.time_next <= self.time_now:
                        print("Start periodic check corp\\alliance mails..")
                        await self.mail_check()
                else:
                    self.time_now = datetime.datetime.now().replace(microsecond=0)
                    self.time_next = self.time_now + datetime.timedelta(seconds=config.evemails["check_interval"])
                    self.time_next = time.mktime(self.time_now.timetuple())
                    await self.cnx.storage_add("nextMailCheck", self.time_next)

                del self.cnx
                await asyncio.sleep(self.interval)
        except Exception as e:
            print(e)
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.mail_task())
        except asyncio.CancelledError as e:
            print(e)
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.mail_task())

    async def mail_check(self):
        try:
            while not self.broadsword.is_closed:
                self.cnx = DBMain()
                self.latestMailID = await self.cnx.storage_get("latestMailID")
                #print("Latest checked mailID {}".format(self.latestMailID))
                if self.latestMailID is None:
                    self.latestMailID = "0"
                self.maxID = self.latestMailID
                self.url = "https://api.eveonline.com/char/MailMessages.xml.aspx?keyID={0}&vCode={1}&characterID={2}" \
                            .format(config.evemails["keyID"], config.evemails["vCode"], config.evemails["characterID"])
                self.mails = await EVEBasic.make_api_request(self.url)
                self.mails = await MailUtils.xml_to_dict(self.mails, "mails")
                if self.mails is not None:
                    for self.mail in self.mails:
                        if (self.mail["@toCorpOrAllianceID"] in config.evemails["fromIDs"]) and (self.mail["@messageID"] > self.maxID):
                            self.url = "https://api.eveonline.com/char/MailBodies.xml.aspx?keyID={0}&vCode={1}&characterID={2}&ids={3}"\
                                            .format(config.evemails["keyID"],\
                                                    config.evemails["vCode"],\
                                                    config.evemails["characterID"],\
                                                    self.mail["@messageID"]\
                                                    )
                            self.content = await EVEBasic.make_api_request(self.url)
                            self.content = await MailUtils.xml_to_dict(self.content, "content")
                            if self.content is not None:
                                self.content = await MailUtils.format_mailbody(self.content)
                                self.msg_split = await MailUtils.str_split(self.content, 1800)

                                self.msg = "**------------------------------------**\n"
                                self.msg += "**Mail By: **{}\n".format(self.mail["@senderName"])
                                self.msg += "**Sent Date: **{}\n".format(self.mail["@sentDate"])
                                self.msg += "**Title: ** {}\n".format(self.mail["@title"])
                                self.msg += "**Content: **\n"
                                self.msg += self.msg_split[0]

                                await self.cnx.message_add(self.msg, self.channel)
                                if len(self.msg_split) > 0:
                                    for self.i in range(1, len(self.msg_split)):
                                        await self.cnx.message_add(self.msg_split[self.i], self.channel)
                                self.maxID = max(self.mail["@messageID"], self.maxID)
                    #print("Latest mailID is {}".format(self.maxID))
                    if self.maxID > self.latestMailID:
                        await self.cnx.storage_add("latestMailID", self.maxID)

                    self.time_now = datetime.datetime.now().replace(microsecond=0)
                    self.time_next = self.time_now + datetime.timedelta(seconds=config.evemails["check_interval"])
                    self.time_next = time.mktime(self.time_next.timetuple())
                    await self.cnx.storage_update("nextMailCheck", self.time_next)
                else:
                    print("EVE ESI is unavailable")
        except Exception as e:
            print(e)
            pass
        finally:
            for attr in ("cnx", "latestMailID", "maxID", "url",
                         "mails", "mail", "content", "msg_split",
                         "msg", "time_now", "time_next"):
                self.__dict__.pop(attr,None)


def setup(broadsword):
    broadsword.add_cog(EVEMail(broadsword))
