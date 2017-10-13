from discord.ext import commands as broadsword
from lib.libeve import EVE_Basic

class EVEApi:
    def __init__(self, broadsword):
        self.broadsword = broadsword

    @broadsword.command(pass_context=True, description='''Это команда получения статуса сервера Tranquility.''')
    async def evestatus(ctx):
        try:
            author = ctx.message.author
            status = await EVE_Basic.getTQOnline()
            stmp = '{0.mention} **TQ Status:**  {1} players online. **Version:** {2}'.format(author, status['userCount'], status['serverVersion'])
            await ctx.say(stmp)
        except:
            await ctx.say('Ошибка при получении статуса сервера Tranquility')



    @broadsword.command()
    async def hello(self, ctx):
        """*hello
        A command that will respond with a random greeting.
        """

        choices = ('Hey!', 'Hello!', 'Hi!', 'Hallo!', 'Bonjour!', 'Hola!')
        await ctx.send(random.choice(choices))

def setup(broadsword):
    broadsword.add_cog(EVEApi(broadsword))