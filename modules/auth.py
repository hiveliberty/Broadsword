from discord.ext import commands as broadsword
from lib.libdb import db
import random

class Auth:
    def __init__(self, bot, db):
        self.broadsword = bot
        self.db = db

    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def test(self, ctx):
        """*hello
        A command that will respond with a random greeting.
        """

        choices = ('Hey!', 'Hello!', 'Hi!', 'Hallo!', 'Bonjour!', 'Hola!')
        await self.broadsword.say(random.choice(choices))

    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def dbtest(self, ctx):
        iscon = self.db.isconnected(self)
        await self.broadsword.say(iscon)

def setup(broadsword):
    broadsword.add_cog(Auth(broadsword, db))