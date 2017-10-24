#import urllib.parse as urllib
from discord.ext import commands as broadsword
from lib.libeve import EVEBasic
from lib.libeve import EVEApi
from lib.libeve import zKillboardAPI

class EVE_API:
    def __init__(self, bot):
        self.broadsword = bot

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
            self.api = EVEApi()
            self.charID = await self.api.getCharID(name)
            self.zapi = zKillboardAPI(self.charID)
            self.response = await self.api.getCharDetails(self.charID)
            self.starsystemID = await self.zapi.getLatestSystem()
            self.shiptypeID = await self.zapi.getLastShipTypeID()
            self.lastseen = await self.zapi.getLastSeenDate()
            self.lastkillmailID = await self.zapi.getLastKillmailID()
            #print("{}\n{}\n{}".format(self.starsystemID, self.shiptypeID, self.lastseen))
            self.msg += '{0.mention}\n```Character info:\n'.format(self.author)
            self.msg += 'Name: {}\n'.format(self.response.name)
            self.msg += 'Birthday: {}\n'.format(self.response.birthday)
            self.msg += 'Alliance: {}\n'.format(await self.api.getAllianceName(self.response.alliance_id))
            self.msg += 'Corporation: {}\n'.format(await self.api.getCorpName(self.response.corporation_id))
            self.msg += 'Last Seen In System: {}\n'.format(await self.api.getSystemName(self.starsystemID))
            self.msg += 'Last Seen Flying a: {}\n'.format(await self.api.getApiTypeName(self.shiptypeID))
            self.msg += 'Last Seen On: {}```\n'.format(self.lastseen)
            self.msg += 'Latest Killmail: https://zkillboard.com/kill/{}/\n'.format(self.lastkillmailID)
            self.msg += 'zKillboard Link: https://zkillboard.com/character/{}/'.format(self.charID)
            await self.broadsword.say(self.msg)
        except:
            await self.broadsword.say('Ошибка\n```{}```'.format(self.response))

    @broadsword.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def testapi(self, ctx, *, name):
        try:
            self.author = ctx.message.author
            self.api = EVEApi()
            self.response = await self.api.getApiMoonName(name)
            self.stmp = '{0.mention}\n```Content:\n {1}```'.format(self.author, self.response)
            await self.broadsword.say(self.stmp)
            #del self.api
            #del self.stmp
        except:
            await self.broadsword.say('Ошибка\n```{}```'.format(self.response))

def setup(broadsword):
    broadsword.add_cog(EVE_API(broadsword))