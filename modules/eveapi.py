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
        #self.name = name
        try:
            self.author = ctx.message.author
            self.api = EVEApi()
            self.charID = await self.api.searchCharID(name)
            self.response = await self.api.getCharDetails(self.charID)
            self.stmp = '{0.mention}\nCharacter info:\nName: {1}\nBirthday: {2}\nAlliance: {3}\nCorporation: {4}\nzKillboard: https://zkillboard.com/character/{5}/'.format(self.author, self.response.name, self.response.birthday, self.response.alliance_id, self.response.corporation_id, self.charID)
            await self.broadsword.say(self.stmp)
        except:
            await self.broadsword.say('Ошибка\n```{}```'.format(self.response))

    @broadsword.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def testapi(self, ctx, *, name):
        try:
            self.author = ctx.message.author
            self.api = zKillboardAPI(name)
            self.response = await self.api.getLastShipTypeID()
            self.stmp = '{0.mention}\n```Content:\n {1}```'.format(self.author, self.response)
            del self.api
            await self.broadsword.say(self.stmp)
        except:
            await self.broadsword.say('Ошибка\n```{}```'.format(self.response))

def setup(broadsword):
    broadsword.add_cog(EVE_API(broadsword))