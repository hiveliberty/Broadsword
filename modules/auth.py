from discord.ext import commands as broadsword
from lib.libdb import DB as DB
from config.config import db as db_conf
import random

class Auth:
    def __init__(self, bot, db, dbconf):
        self.broadsword = bot
        self.DB = db
        self.dbconf = dbconf

    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def test(self, ctx):
        """*hello
        A command that will respond with a random greeting.
        """

        choices = ('Hey!', 'Hello!', 'Hi!', 'Hallo!', 'Bonjour!', 'Hola!')
        await self.broadsword.say(random.choice(choices))

    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def dbversion(self, ctx):
        try:
            self.test = self.DB(self.dbconf)
            self.result = self.test.request("SELECT version();")
            print(self.result[0][0])
            await self.broadsword.say("```{}```".format(self.result[0][0]))
        except:
            self.broadsword.say("Oooops")
        else:
            del self.test

def setup(broadsword):
    broadsword.add_cog(Auth(broadsword, DB, db_conf))