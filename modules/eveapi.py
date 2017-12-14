#import urllib.parse as urllib
import time
import json
import xmltodict
import logging
from discord.ext import commands as broadsword
from importlib import reload
from lib import utils
from lib.db import DBMain
from lib.eve import EVEBasic
from lib.eve import EVEApi
from lib.eve import zKillboardAPI
from config import config

log = logging.getLogger(__name__)

class EVE_API:
    def __init__(self, bot):
        self.broadsword = bot

    @broadsword.group(pass_context=True, hidden=False, description='''Группа команд администратора.''')
    async def eveapiadmin(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say("{0.mention}, invalid git command passed...".format(self.author))

    @eveapiadmin.command(pass_context=True)
    async def reloadconf(self, ctx):
        try:
            reload(config)
        except Exception as e:
            print(e)
            await self.broadsword.say("Oooops")

    @broadsword.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def evestatus(self, ctx):
        try:
            self.author = ctx.message.author
            self.status = await EVEBasic.getTQOnline()
            self.stmp = '{0.mention} **TQ Status:**  {1} players online. **Version:** {2}'.format(self.author, self.status['userCount'], self.status['serverVersion'])
            await self.broadsword.say(self.stmp)
        except:
            await self.broadsword.say('Ошибка при получении статуса сервера Tranquility')
            
    @broadsword.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def tq(self, ctx):
        try:
            self.author = ctx.message.author
            self.api = EVEApi()
            self.response = await self.api.statusTQ()
            self.stmp = '{0.mention}\n**TQ Status:**  {1} players online.\n**Version:** {2}'.format(self.author, self.response.players, self.response.server_version)
            await self.broadsword.say(self.stmp)
        except:
            await self.broadsword.say('Ошибка при получении статуса сервера Tranquility\n```{}```'.format(self.response))

    @broadsword.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def charinfo(self, ctx, *, name):
        try:
            self.author = ctx.message.author
            self.msg = ''
            self.eve_api = EVEApi()
            self.charID = await self.eve_api.getCharID(name)
            self.zkill_api = zKillboardAPI(self.charID)
            self.response = await self.eve_api.getCharDetails(self.charID)
            #self.conpinfo = await self.eve_api.getCharDetails(self.response.corporation_id)
            #print(self.conpinfo)
            print(self.response.corporation_id)
            self.starsystemID = await self.zkill_api.getLatestSystem()
            self.shiptypeID = await self.zkill_api.getLastShipType()
            self.lastseen = await self.zkill_api.getLastSeenDate()
            self.lastkillmailID = await self.zkill_api.getLastKillmailID()
            self.birthday = time.strptime(self.response.birthday[:19], "%Y-%m-%dT%H:%M:%S")
            self.birthday = time.strftime("%d.%m.%Y at %H:%M:%S", self.birthday)
            self.msg += '{0.mention}\n```Character info:\n'.format(self.author)
            self.msg += 'Name: {}\n'.format(self.response.name)
            self.msg += 'Birthday: {}\n'.format(self.birthday)
            self.msg += 'Alliance: {}\n'.format(await self.eve_api.getAllianceName(self.response.alliance_id))
            self.msg += 'Corporation: {}\n'.format(await self.eve_api.getCorpName(self.response.corporation_id))
            #self.msg += 'Corporation: {}\n'.format(self.conpinfo.name])
            self.msg += 'Last Seen In System: {}\n'.format(self.starsystemID)
            self.msg += 'Last Seen Flying a: {}\n'.format(self.shiptypeID)
            self.msg += 'Last Seen On: {}```'.format(self.lastseen)
            self.msg += 'Latest Killmail: https://zkillboard.com/kill/{}/\n'.format(self.lastkillmailID)
            self.msg += 'zKillboard Link: https://zkillboard.com/character/{}/'.format(self.charID)
            await self.broadsword.say(self.msg)
        except:
            await self.broadsword.say('Ошибка\n```{}```'.format(self.response))
        else:
            del self.msg
            del self.eve_api
            del self.zkill_api


def setup(broadsword):
    broadsword.add_cog(EVE_API(broadsword))
