import asyncio
import random
from discord.ext import commands as broadsword
#from lib.libdb import DBAuth as DBAuth
#from lib import libdb as dbclasses
from lib.libeve import EVEApi
from lib.libdb import DB
#from config.config import db as db_conf
from config import config

class Auth:
    def __init__(self, bot):
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
        self.roles = ''
        self.todelete = [ctx.message]
        self.author = ctx.message.author
        self.code = code
        self.messages_single = False
        try:
            if len(self.code) < 12:
                self.messages_single = True
                await self.broadsword.say("{0.mention}, invalid code! Check your auth code and try again.".format(self.author))
                return None

            self.cnx = DB()
            self.pending = await self.cnx.selectPending(self.code)
            #   self.pending content:
            #       'authString'
            #       'allianceID'
            #       'corporationID'
            #       'characterID'
            #       'dateCreated'
            #       'id'
            #       'active'
            del self.cnx

            self.corpinfo = await self.eveapi.getCorpDetails(self.result['corporationID'])
            #   self.corpinfo content:
            #       'alliance_id'
            #       'ceo_id'
            #       'corporation_description'
            #       'corporation_name'
            #       'creation_date'
            #       'creator_id'
            #       'faction'
            #       'member_count'
            #       'tax_rate'
            #       'ticker'
            #       'url'

            #   Say to channel
            self.bot_answer = await self.broadsword.say("```{0}\n{1}\n{2}\n{3}```".format(self.author, self.code, self.todelete, self.pending))
            self.todelete.append(self.bot_answer)
        except:
            self.broadsword.say("Oooops")
        finally:
            await asyncio.sleep(10)
            if not self.messages_single:
                await self.broadsword.delete_messages(self.todelete)
            else:
                await self.broadsword.delete_message(ctx.message)
            del self.auth

def setup(broadsword):
    #broadsword.add_cog(Auth(broadsword, DBAuth, db_conf))
    #broadsword.add_cog(AuthTemp(broadsword, dbclasses))
    broadsword.add_cog(AuthTemp(broadsword))