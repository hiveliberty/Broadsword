from discord.ext import commands as broadsword
#from lib.libdb import DBAuth as DBAuth
from lib import libdb as dbclasses
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
            
    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def addtestuser(self, ctx):
        self.testCharID = "94074030"
        self.testCorpID = "98014265"
        self.testAllianceID = "1614483120"
        self.testGroups = ""
        self.testAuthString = "58512d6c9c68a"
        self.testActive = "1"
        try:
            self.test = self.DB(self.dbconf)
            self.test.insertTestUser(self.testCharID, self.testCorpID, self.testAllianceID, self.testGroups, self.testAuthString, self.testActive)
            await self.broadsword.say("```User added.```")
        except:
            self.broadsword.say("Oooops")
        else:
            del self.test

    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def auth(self, ctx, code):
        self.code = code
        try:
            self.test = self.DB(self.dbconf)
            self.result = self.test.selectPending(self.code)
            await self.broadsword.say("```{}```".format(self.result))
        except:
            self.broadsword.say("Oooops")
        else:
            del self.test
            
class AuthTemp:
    def __init__(self, bot, dbclasses):
        self.broadsword = bot
        self.dbclasses = dbclasses

    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def test(self, ctx):
        """A command that will respond with a random greeting."""

        choices = ('Hey!', 'Hello!', 'Hi!', 'Hallo!', 'Bonjour!', 'Hola!')
        await self.broadsword.say(random.choice(choices))

    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def addtestuser(self, ctx):
        self.testCharID = "94074030"
        self.testCorpID = "98014265"
        self.testAllianceID = "1614483120"
        self.testGroups = ""
        self.testAuthString = "58512d6c9c68a"
        self.testActive = "1"
        try:
            self.cnx = self.dbclasses.DBAuth()
            self.cnx.insertTestUser(self.testCharID, self.testCorpID, self.testAllianceID, self.testGroups, self.testAuthString, self.testActive)
            await self.broadsword.say("```User added.```")
        except:
            self.broadsword.say("Oooops")
        else:
            del self.cnx

    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def auth(self, ctx, code):
        self.code = code
        try:
            self.cnx = self.dbclasses.DBAuth()
            self.result = self.cnx.selectPending(self.code)
            await self.broadsword.say("```{}```".format(self.result))
        except:
            self.broadsword.say("Oooops")
        else:
            del self.cnx

def setup(broadsword):
    #broadsword.add_cog(Auth(broadsword, DBAuth, db_conf))
    broadsword.add_cog(AuthTemp(broadsword, dbclasses))