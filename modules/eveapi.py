from discord.ext import commands as broadsword
from lib.libeve import EVEBasic

class EVEApi:
    def __init__(self, bot):
        self.broadsword = bot

    @broadsword.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def evestatus(self, ctx):
        try:
            author = ctx.message.author
            status = await EVEBasic.getTQOnline()
            stmp = '{0.mention} **TQ Status:**  {1} players online. **Version:** {2}'.format(author, status['userCount'], status['serverVersion'])
            await self.broadsword.say(stmp)
        except:
            await self.broadsword.say('Ошибка при получении статуса сервера Tranquility')

def setup(broadsword):
    broadsword.add_cog(EVEApi(broadsword))