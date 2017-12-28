#import urllib.parse as urllib
import time
import json
import datetime
import logging
import asyncio
from operator import itemgetter
from discord.ext import commands as broadsword

from lib.utils import MailUtils
from lib.db import DBMain
from lib.esi import ESIApi
from lib.token import EVEToken
#from lib.libeve import zKillboardAPI
from config import config

log = logging.getLogger(__name__)


class Test:
    def __init__(self, bot):
        self.broadsword = bot

    async def _selfclean(self, vars):
        for attr in vars: self.__dict__.pop(attr,None)

    @broadsword.group(pass_context=True, hidden=False, description='''Группа тестовых команд.''')
    async def test(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say("{0.mention}, invalid test command passed...".format(ctx.message.author))

    @test.command(name="token", pass_context=True, description='''Описание отсутствует.''')
    async def _token(self, ctx):
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
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
            #await self.broadsword.say("Ошибка\n```{}```".format(e))
        #finally:
        #    del self.cnx

    @test.command(name="token2", pass_context=True, description='''Тестовая команда.''')
    async def _token2(self, ctx):
        try:
            self.token_api = EVEToken()
            self.token = await self.token_api.get_token()
            log.info("Your access token: {}".format(self.token))
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(("token_api", "expired"))

    @test.command(pass_context=True, description='''Тестовая команда.''')
    async def time(self, ctx):
        try:
            self.now = datetime.datetime.now().replace(microsecond=0)
            self.unix_time = time.mktime(self.now.timetuple())
            self.unix_time = str(self.unix_time)
            self.unix_time = float(self.unix_time)
            self.now2 = datetime.datetime.fromtimestamp(self.unix_time)
            await self.broadsword.say("```{0}\n{1}\n{2}```".format(self.now, self.unix_time, self.now2))
            print(self.token)
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("token_api", "expired"):
                self.__dict__.pop(attr,None)

    @test.command(pass_context=True, description='''Тестовая команда.''')
    async def db(self, ctx):
        try:
            self.cnx = DBMain()
            self.msg_id = await self.cnx.message_get_oldest()
            self.msg = await self.cnx.message_get(self.msg_id)
            log.info(self.msg)
            await self.broadsword.say("```{}```".format(self.msg))
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("cnx", "temp_value"):
                self.__dict__.pop(attr,None)

    @test.command(pass_context=True, description='''Тестовая команда.''')
    async def esi(self, ctx, *, str):
        try:
            self.esi = ESIApi()
            self.esi_data = await self.esi.char_get_id(str)
            log.info(self.esi_data)
            await self.broadsword.say("```{}```".format(self.esi_data))
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(("esi", "esi_data"))

    @test.command(pass_context=True, description='''Тестовая команда.''')
    async def mailbody(self, ctx, mail_id):
        try:
            self.token_api = EVEToken(config.sso["character_id"])
            self.token = await self.token_api.get_token()
            self.esi = ESIApi()
            self.body = await self.esi.mails_get_mail(
                config.sso["character_id"], mail_id, self.token
            )
            await self.broadsword.say("```{}```".format(self.body))
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(("token_api", "token", "esi", "body"))


def setup(broadsword):
    broadsword.add_cog(Test(broadsword))
