#import urllib.parse as urllib
import time
import json
import datetime
from operator import itemgetter
from discord.ext import commands as broadsword
from lib.utils import MailUtils
from lib.libdb import DBMain
from lib.libeve import EVEBasic
from lib.libeve import EVEApi
from lib.libtoken import EVEToken
#from lib.libeve import zKillboardAPI
from config import config

class Test():
    def __init__(self, bot):
        self.broadsword = bot

    @broadsword.group(pass_context=True, hidden=False, description='''Группа команд администратора.''')
    async def test(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say("{0.mention}, invalid test command passed...".format(ctx.author))

    @test.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def code(self, ctx):
        try:
            self.token_api = EVEToken()
            self.token = await self.token_api.token()
            self.eve_api = EVEApi(self.token)
            self.mails = await self.eve_api.get_mails()
            for i in range(0, len(self.mails)):
                self.mails[i] = self.mails[i].to_dict()
            print(self.mails)
            self.mails = self.mails.sort(key=itemgetter('timestamp'))
            print(self.mails)
            #print(config.credentials["api_key"]["character_id"])
        except Exception as e:
            print(e)
            #await self.broadsword.say("Ошибка\n```{}```".format(e))
        #finally:
        #    del self.cnx

    @test.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def code2(self, ctx):
        try:
            self.token_api = EVEToken()
            self.expired = await self.token_api.expired()
            if self.expired:
                print("Token is expired")
            else:
                print("Token is not expired")
            #print(locals())
        except Exception as e:
            print(e)
        finally:
            for attr in ("token_api", "expired"):
                self.__dict__.pop(attr,None)

    @test.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def code3(self, ctx):
        try:
            self.token_api = EVEToken()
            self.token = await self.token_api.token()
            print(self.token)
        except Exception as e:
            print(e)
        finally:
            for attr in ("token_api", "expired"):
                self.__dict__.pop(attr,None)


def setup(broadsword):
    broadsword.add_cog(Test(broadsword))
