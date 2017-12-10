import sys
import asyncio
import discord
from discord.ext import commands as broadsword
#import xmltodict
from lib.utils import MailUtils
from lib.libdb import DBMain
from lib.libeve import EVEBasic
from config import config


class EVEMail:
    def __init__(self, bot):
        self.broadsword = bot
        #self.server = self.broadsword.get_server(id=config.bot["guild"])
        self.interval = 300
        self.channel = config.evemails["channelID"]
        self._task = self.broadsword.loop.create_task(self.mail_task())
        print('MailTask should have been run in background..')
        
    def __unload(self):
        self._task.cancel()
        print('MailTask should have been unloaded..')
        
    async def mail_task(self):
        try:
            while not self.broadsword.is_closed:
                print("Start periodic check corp\\alliance mails..")
                self.cnx = DBMain()
                self.latestMailID = await self.cnx.storage_get("latestMailID");
                print("Latest checked mailID {}".format(self.latestMailID))
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
                    print("Latest mailID is {}".format(self.maxID))
                    if self.maxID > self.latestMailID:
                        await self.cnx.storage_add("latestMailID", self.maxID)
                else:
                    print("EVE ESI is unavailable")
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

def setup(broadsword):
    broadsword.add_cog(EVEMail(broadsword))
