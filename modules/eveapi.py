#import urllib.parse as urllib
import datetime
import discord
import json
import logging
import time
import xmltodict
from discord.ext import commands as broadsword
from importlib import reload

from lib import utils
from lib.db import DBMain
#from lib.eve import EVEBasic
from lib.esi import ESIApi
from lib.zkillboard import zKillboardAPI
from config import config

log = logging.getLogger(__name__)

class EVE_API:
    def __init__(self, bot):
        self.broadsword = bot

    async def _selfclean(self, vars):
        for attr in vars: self.__dict__.pop(attr,None)

    @broadsword.group(pass_context=True, hidden=False, description='''Группа команд секции EVE Api.''')
    async def eveapi(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say("{0.mention}, invalid command passed...".format(self.author))

    @eveapi.command(pass_context=True, hidden=False)
    async def reloadconf(self, ctx):
        try:
            reload(config)
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
            await self.broadsword.say("Oooops! I cann't reload config!")

    @broadsword.command(name="tq",pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def _tq(self, ctx):
        try:
            self.author = ctx.message.author
            self.api = ESIApi()
            self.response = await self.api.status_tq()
            self.stmp = "{.mention}".format(self.author) +\
                        "\n**TQ Status:** {} players online.".format(self.response["players"]) +\
                        "\n**Version:** {}".format(self.response["server_version"])
            await self.broadsword.say(self.stmp)
        except Exception:
            await self.broadsword.say("Ошибка при получении статуса сервера Tranquility.")
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("author", "api", "response", "stmp"):
                self.__dict__.pop(attr,None)

    @broadsword.command(pass_context=True, description='''Команда получения информации о персонаже.''')
    async def charinfo(self, ctx, *, name):
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
            await self.broadsword.say("Cann't get character information. Something wrong.")
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(
                ("msg", "esi", "zkill_api", "author", "char_id", "response",
                 "starsystemID", "shiptypeID", "lastseen", "lastkillmailID",
                 "birthday")
            )


def setup(broadsword):
    broadsword.add_cog(EVE_API(broadsword))
