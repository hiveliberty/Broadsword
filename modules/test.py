#import urllib.parse as urllib
import time
import json
from discord.ext import commands as broadsword
from lib.utils import MailUtils
from lib.libdb import DB
from lib.libeve import EVEBasic
#from lib.libeve import EVEApi
#from lib.libeve import zKillboardAPI
from config import config

class Test:
    def __init__(self, bot):
        self.broadsword = bot

    @broadsword.group(pass_context=True, hidden=False, description='''Группа команд администратора.''')
    async def test(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say("{0.mention}, invalid test command passed...".format(ctx.author))

    @test.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def code(self, ctx):
        try:
            self.cnx = DB()
            self.latestMailID = await self.cnx.getKey("latestMailID");
            print(self.latestMailID)
            if self.latestMailID is None:
                self.latestMailID = "0"
            self.maxID = self.latestMailID
            self.server = self.broadsword.get_server(id=config.bot["guild"])
            self.url = "https://api.eveonline.com/char/MailMessages.xml.aspx?keyID={0}&vCode={1}&characterID={2}" \
                        .format(config.evemails["keyID"], config.evemails["vCode"], config.evemails["characterID"])
            self.mails = await EVEBasic.makeApiRequest(self.url)
            self.mails = await MailUtils.xml_to_dict(self.mails, "mails")
            if self.mails is not None:
                print(self.mails)
                self.ix = 0
                for self.mail in self.mails:
                    print(self.ix)
                    if (self.mail["@toCorpOrAllianceID"] in config.evemails["fromIDs"]) and (self.mail["@messageID"] > self.maxID):
                        print(self.maxID)
                        print(self.mail["@messageID"])
                        print(self.mail["@toCorpOrAllianceID"])
                        print("---")
                        self.url = "https://api.eveonline.com/char/MailBodies.xml.aspx?keyID={0}&vCode={1}&characterID={2}&ids={3}"\
                                        .format(config.evemails["keyID"],\
                                                config.evemails["vCode"],\
                                                config.evemails["characterID"],\
                                                self.mail["@messageID"]\
                                                )
                        self.content = await EVEBasic.makeApiRequest(self.url)
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

                            await self.cnx.addQueueMessage(self.msg, ctx.message.channel.id)
                            if len(self.msg_split) > 0:
                                for self.i in range(1, len(self.msg_split)):
                                    print(self.msg_split[self.i])
                                    await self.cnx.addQueueMessage(self.msg_split[self.i], ctx.message.channel.id)
                            self.maxID = max(self.mail["@messageID"], self.maxID)
                            print(self.maxID)
                            print("---")
                    self.ix += 1
                print("Latest mailID is {}".format(self.maxID))
                if self.maxID > self.latestMailID:
                    print("true")
                    await self.cnx.setKey("latestMailID", self.maxID)
            else:
                print("EVE ESI is unavailable")
        except Exception as e:
            print(e)
            #await self.broadsword.say("Ошибка\n```{}```".format(e))
        finally:
            del self.cnx

    @test.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def code2(self, ctx):
        try:
            self.url = "https://api.eveonline.com/char/MailMessages.xml.aspx?keyID={0}&vCode={1}&characterID={2}" \
                        .format(config.evemails["keyID"], config.evemails["vCode"], config.evemails["characterID"])
            self.mails = await EVEBasic.makeApiRequest(self.url)
            self.mails = await MailUtils.xml_to_dict(self.mails, "mails")
            if self.mails is not None:
                for self.mail in self.mails:
                    #if self.mail["@messageID"] == "0":
                    #if self.mail["@messageID"] == "0":
                    if self.mail["@messageID"] == "0":
                        print("X")
                        break

            self.mailID = self.mail["@messageID"]
            self.url = "https://api.eveonline.com/char/MailBodies.xml.aspx?keyID={0}&vCode={1}&characterID={2}&ids={3}"\
                        .format(config.evemails["keyID"],\
                                config.evemails["vCode"],\
                                config.evemails["characterID"],\
                                self.mailID\
                                )
            self.content = await EVEBasic.makeApiRequest(self.url)
            self.content = await MailUtils.xml_to_dict(self.content, "content")
            print("Content before format:\n{}".format(self.content))
            self.content = await MailUtils.format_mailbody(self.content)
            print("Content after format:\n{}".format(self.content))
            #self.msg_split = await MailUtils.str_split(self.content, 620)

            self.msg = "**------------------------------------**\n"
            self.msg += "**Mail By: **{}\n".format(self.mail["@senderName"])
            self.msg += "**Sent Date: **{}\n".format(self.mail["@sentDate"])
            self.msg += "**Title: ** {}\n".format(self.mail["@title"])
            self.msg += "**Content: **\n"
            #self.msg += self.msg_split[0]
            self.msg += str(self.content)

            self.cnx = DB()
            await self.cnx.addQueueMessage(self.msg, ctx.message.channel.id)
            #if len(self.msg_split) > 0:
            #    for self.i in range(1, len(self.msg_split)):
            #        await self.cnx.addQueueMessage(self.msg_split[self.i], ctx.message.channel.id)
            #await self.broadsword.say('{}'.format(self.msg_split))
        except Exception as e:
            print(e)
            await self.broadsword.say('Ошибка\n```{}```'.format(self.content))
        finally:
            del self.cnx

    @test.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def code3(self, ctx):
        try:
            self.url = "https://api.eveonline.com/char/MailMessages.xml.aspx?keyID={0}&vCode={1}&characterID={2}" \
                        .format(config.evemails["keyID"], config.evemails["vCode"], config.evemails["characterID"])
            self.mails = await EVEBasic.makeApiRequest(self.url)
            self.mails = await MailUtils.xml_to_dict(self.mails, "test")
            print(self.mails)
            #self.maxID = "0"
            #self.maxID = max("34", "33", "45", self.maxID)
            #await self.broadsword.say("{}".format(self.maxID))
        except Exception as e:
            print(e)

def setup(broadsword):
    broadsword.add_cog(Test(broadsword))