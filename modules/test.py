#import urllib.parse as urllib
import time
import json
from discord.ext import commands as broadsword
from lib.utils import MailUtils
from lib.libdb import DBMain
from lib.libeve import EVEBasic
from lib.libeve import EVEApi
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
            self.eve_api = EVEApi()
            self.mails = await self.eve_api.get_mails(config.credentials["eve_token"])
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
            pass
        except Exception as e:
            print(e)
            await self.broadsword.say('Ошибка\n```{}```'.format(self.content))
        finally:
            del self.cnx

    @test.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def code3(self, ctx):
        try:
            pass
        except Exception as e:
            print(e)

def setup(broadsword):
    broadsword.add_cog(Test(broadsword))
