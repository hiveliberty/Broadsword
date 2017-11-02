import asyncio
import random
import sys
from discord.ext import commands as broadsword
#from lib.libdb import DBAuth as DBAuth
#from lib import libdb as dbclasses
from lib.libeve import EVEApi
from lib.libdb import DB
#from config.config import db as db_conf
from config import config

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
        #self.todelete = [ctx.message]
        self.author = ctx.message.author
        self.code = code
        self.failed = False

        try:
            if len(self.code) < 12:
                self.failed = True
                await self.broadsword.say("{0.mention}, invalid code! Check your auth code and try again.".format(self.author))

            if not self.failed:
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
                if self.pending == None:
                    self.failed = True
                    await self.broadsword.say("{0.mention}, not existing auth code!".format(self.author))

            if not self.failed:
                self.corpinfo = await self.eveapi.getCorpDetails(self.pending['corporationID'])
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
            if not self.failed:
                self.bot_answer = await self.broadsword.say("```{0}\n{1}\n{2}```".format(self.author, self.code, self.pending))
                #self.todelete.append(self.bot_answer)
        except Exception as e:
            print(e)
            await self.broadsword.say("{0.mention}, ooops! Something wrong!".format(self.author))
        finally:
            await asyncio.sleep(2)
            await self.broadsword.delete_message(ctx.message)
            del self.author
            del self.code
            #if 'self.pending' in locals():
            if not self.failed:
                del self.pending
            #if 'self.corpinfo' in locals():
            if not self.failed:
                del self.corpinfo
            #if 'self.bot_answer' in locals():
            if not self.failed:
                del self.bot_answer

def setup(broadsword):
    #broadsword.add_cog(Auth(broadsword, DBAuth, db_conf))
    #broadsword.add_cog(AuthTemp(broadsword, dbclasses))
    broadsword.add_cog(AuthTemp(broadsword))