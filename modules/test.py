#import urllib.parse as urllib
import asyncio
import datetime
import discord
import json
import logging
import time
from discord.ext import commands as broadsword
from operator import itemgetter

from lib.utils import MailUtils
from lib.db import DBMain
from lib.esi import ESIApi
from lib.token import EVEToken
from lib.zkillboard import zKillboardAPI
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

    @test.command(name="embed", pass_context=True, description='''Тестовая команда.''')
    async def _embed(self, ctx, *, name):
        try:
            self.esi = ESIApi()
            self.char_id = await self.esi.char_get_id(name)
            if len(self.char_id) == 1:
                self.char_id = self.char_id[0]

            self.zkill_api = zKillboardAPI(self.char_id)
            self.char_info = await self.esi.char_get_details(self.char_id)

            self.star_system_id = await self.zkill_api.system_get_latest()
            self.ship_type_id = await self.zkill_api.shiptype_get_last()
            self.last_seen = await self.zkill_api.seendate_get_last()
            if self.last_seen is None:
                self.last_seen = "Unknown"
            self.killmail_last_id = await self.zkill_api.killmail_id_get_last()
            self.corp_name = await self.esi.corp_get_name(
                self.char_info["corporation_id"])

            self.birthday = time.strptime(self.char_info["birthday"][:19], "%Y-%m-%dT%H:%M:%S")
            self.birthday = time.strftime("%d.%m.%Y at %H:%M:%S", self.birthday)

            self.desc = "**Birthday:** {}\n".format(self.birthday) +\
                        "**Corporation:** {}\n".format(self.corp_name) +\
                        "**Last Seen In System:** {}\n".format(self.star_system_id) +\
                        "**Last Seen Flying at:** {}\n".format(self.ship_type_id) +\
                        "**Last Seen On:** {}\n".format(self.last_seen) +\
                        "**Latest Killmail:** https://zkillboard.com/kill/{}/\n".\
                        format(self.killmail_last_id)

            self.embed = discord.Embed(
                title="{}".format(self.char_info["name"]),
                description=self.desc,
                url="https://zkillboard.com/character/{}/".format(self.char_id),
                color=0xe25822
            )
            self.embed.set_thumbnail(
                url="https://imageserver.eveonline.com/Character/{}_256.jpg".\
                format(self.char_id)
            )
            self.embed.set_footer(text=datetime.datetime.now().replace(microsecond=0))

            await self.broadsword.say(embed=self.embed)
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(("token_api", "token", "esi", "body"))


def setup(broadsword):
    broadsword.add_cog(Test(broadsword))
