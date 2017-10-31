import asyncio
import random
from discord.ext import commands as broadsword
#from lib.libdb import DBAuth as DBAuth
#from lib import libdb as dbclasses
from lib.libeve import EVEApi
from lib.libdb import DB
from config.config import db as db_conf

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
    #def __init__(self, bot, dbclasses):
    def __init__(self, bot):
        self.broadsword = bot
        self.eveapi = EVEApi()
        #self.dbclasses = dbclasses

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
        self.testAuthString = "58512d6c9c68a"
        self.testActive = "1"
        try:
            #self.cnx = self.dbclasses.DB()
            self.cnx = DB()
            await self.cnx.insertTestUser(self.testCharID, self.testCorpID, self.testAllianceID, self.testAuthString, self.testActive)
            await self.broadsword.say("```User added.```")
        except:
            self.broadsword.say("Oooops")
        else:
            del self.cnx

    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def auth(self, ctx, code):
        self.messages_todelete = [ctx.message]
        self.msg_author = ctx.message.author
        self.code = code
        self.messages_single = False
        try:
            if len(self.code) < 12:
                self.messages_single = True
                await self.broadsword.say("{0.mention}, invalid code! Check your auth code and try again.".format(self.msg_author))
                return None
            #self.cnx = self.dbclasses.DB()
            self.cnx = DB()
            self.result = await self.cnx.selectPending(self.code)
            del self.cnx
            self.corpinfo = await self.eveapi.getCorpDetails(self.result['corporationID'])
            #print(self.corpinfo['ticker'])
            #print(self.corpinfo['corporation_name'])
            #print("test endpoint 01")
            #await self.broadsword.say("```{}```".format(self.corpinfo))
            print("test endpoint 01")
            self.bot_answer = await self.broadsword.say("```{0}\n{1}\n{2}\n{3}```".format(self.msg_author, self.code, self.messages_todelete, self.result))
            print("test endpoint 02")
            self.messages_todelete.append(self.bot_answer)
            print("test endpoint 03")
        except:
            self.broadsword.say("Oooops")
        finally:
            print("test endpoint 04")
            await asyncio.sleep(5)
            print("test endpoint 05")
            if not self.messages_single:
                await self.broadsword.delete_messages(self.messages_todelete)
            else:
                await self.broadsword.delete_message(ctx.message)

def setup(broadsword):
    #broadsword.add_cog(Auth(broadsword, DBAuth, db_conf))
    #broadsword.add_cog(AuthTemp(broadsword, dbclasses))
    broadsword.add_cog(AuthTemp(broadsword))