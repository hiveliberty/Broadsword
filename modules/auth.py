from discord.ext import commands as broadsword
import random

class Auth:
    def __init__(self, broadsword):
        self.broadsword = broadsword

    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def test(self, ctx):
        """*hello
        A command that will respond with a random greeting.
        """

        choices = ('Hey!', 'Hello!', 'Hi!', 'Hallo!', 'Bonjour!', 'Hola!')
        await self.broadsword.say(random.choice(choices))

def setup(broadsword):
    broadsword.add_cog(Auth(broadsword))