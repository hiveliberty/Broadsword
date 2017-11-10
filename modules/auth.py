import asyncio
import json
import random
import sys
import discord
from discord.ext import commands as broadsword
#from lib.libdb import DBAuth as DBAuth
#from lib import libdb as dbclasses
from lib.libeve import EVEApi
from lib.libdb import DB
#from config.config import db as db_conf
from config import config

class AuthUser:
    def __init__(self, bot):
        self.broadsword = bot
        self.eveapi = EVEApi()
        self.server = self.broadsword.get_server(id=config.bot['guild'])

    @broadsword.command(pass_context=True, description='''Тестовая команда.''')
    async def test(self, ctx):
        """A command that will respond with a random greeting."""

        choices = ('Hey!', 'Hello!', 'Hi!', 'Hallo!', 'Bonjour!', 'Hola!')
        await self.broadsword.say(random.choice(choices))

    @broadsword.command(pass_context=True, description='''Тестовая команда добавления пользователя для авторизации.''')
    async def addtestuser(self, ctx):
        self.testCharID = "94074030"
        self.testCorpID = "98014265"
        self.testAllianceID = "1614483120"
        self.testAuthString = "58512d6c9c68a"
        self.testActive = "1"
        try:
            self.cnx = DB()
            await self.cnx.insertTestUser(self.testCharID, self.testCorpID, self.testAllianceID, self.testAuthString, self.testActive)
            await self.broadsword.say("```User added.```")
        except:
            await self.broadsword.say("Oooops")
        else:
            del self.cnx

    @broadsword.command(pass_context=True, description='''Тестовая команда добавления в очередь сообщений.''', hidden=True)
    async def addmsg(self, ctx, *, msg):
        self.channel = ctx.message.channel.id
        self.msg = msg
        try:
            self.cnx = DB()
            await self.cnx.addQueueMessage(self.msg, self.channel)
        except:
            await self.broadsword.say("Oooops")
        else:
            del self.cnx

    @broadsword.command(pass_context=True, description='''Тестовая команда добавления в очередь переименования.''', hidden=True)
    async def addrename(self, ctx, id, nick):
        print(id)
        print(nick)
        try:
            self.cnx = DB()
            await self.cnx.addQueueRename(id, nick)
        except:
            await self.broadsword.say("Oooops")
        else:
            del self.cnx

    @broadsword.command(pass_context=True, description='''Команда авторизации.''')
    async def auth(self, ctx, code):
        self.author = ctx.message.author
        self.code = code
        self.failed = False

        try:
            if len(self.code) < 13:
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

                if self.pending == None:
                    self.failed = True
                    await self.broadsword.say("{0.mention}, not existing auth code or you are already authorized!".format(self.author))

            if not self.failed:
                self.auth_roles = []
                self.doAuthorize = False

                self.not_member = True
                for self.group_key, self.group_values in config.auth["authGroups"].items():
                    if self.group_values["id"] == self.pending["allianceID"]:
                        self.not_member = False
                        self.auth_group = self.group_values
                        del self.group_values
                        break
                if self.not_member:
                    await self.broadsword.say("{0.mention}, you are not alliance member!".format(self.author))
                    return

                self.corpinfo = await self.cnx.getCorpInfo(self.pending["corporationID"])
                #   self.corpinfo content:
                #       'id'
                #       'corpID'
                #       'corpTicker'
                #       'corpName'
                #       'corpRole'

                if self.corpinfo is None:
                    self.corpinfo = {}
                    self.corpinfo_temp = await self.eveapi.getCorpDetails(self.pending["corporationID"])
                    #   self.corpinfo_temp content:
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
                    self.corpinfo["corpTicker"] = self.corpinfo_temp["ticker"]
                    self.corpinfo["corpName"] = self.corpinfo_temp["corporation_name"]
                    if config.auth["setCorpRole"] and self.auth_group["type"] == "alliance":
                        self.corpinfo["corpRole"] = self.corpinfo["corpTicker"] + " Members"
                        print("Corp role is '{}'".format(self.corpinfo['corpRole']))
                    else:
                        self.corpinfo["corpRole"] = ""
                        print("Corp role is ''")
                    await self.cnx.addCorpInfo(self.pending["corporationID"], self.corpinfo["corpTicker"], self.corpinfo["corpName"], self.corpinfo["corpRole"])

                if (self.corpinfo["corpRole"] is None or self.corpinfo["corpRole"] == "") and config.auth["setCorpRole"] and self.auth_group["type"] == "alliance":
                    print("setCorpRole has been enabled")
                    self.corpinfo["corpRole"] = self.corpinfo["corpTicker"] + " Members"
                    await self.cnx.addCorpInfo(self.corpinfo["corpID"], self.corpinfo["corpTicker"], self.corpinfo["corpName"], self.corpinfo["corpRole"])

                if config.auth["setCorpRole"] and self.auth_group["type"] == "alliance":
                    self.corp_role_exist = False
                    self.role = None
                    for self.role in self.server.roles:
                        print(self.role.name)
                        if self.role.name == self.corpinfo["corpRole"]:
                            self.corp_role_exist = True
                            self.corp_role = self.role
                            break
                    if not self.corp_role_exist:
                        self.corp_role = await self.broadsword.create_role(
                            self.server,
                            name=self.corpinfo["corpRole"],
                            permissions=discord.Permissions(104324160),
                            colour=discord.Colour(0x1f8b4c),
                            hoist=True,
                            mentionable=True
                        )
                    self.auth_roles.append(self.corp_role)

                self.role = None
                for self.role in self.server.roles:
                    if self.role.name == self.auth_group["memberRole"]:
                        self.auth_roles.append(self.role)
                        self.doAuthorize = True
                        break

                if self.doAuthorize:
                    await self.broadsword.add_roles(self.author, *self.auth_roles)
                    if config.auth["nameEnforce"]:
                        self.charname = ""
                        self.charinfo = await self.eveapi.getCharDetails(self.pending["characterID"])
                        if config.auth["corpTickers"] and self.auth_group["type"] == "alliance":
                            self.charname = "[" + self.corpinfo["corpTicker"] + "] "
                        self.charname = self.charname + self.charinfo["name"]
                        await self.cnx.addQueueRename(self.author.id, self.charname)
                    await self.cnx.disableReg(self.code)
                    await self.cnx.insertUser(self.pending["characterID"], self.author.id, self.charinfo["name"])
                    await self.broadsword.say("{0.mention}, you have been authorized!".format(self.author))
                else:
                    await self.broadsword.say("{0.mention}, you cann't be authorized, because no role is set for auth!".format(self.author))
        except Exception as e:
            print(e)
            await self.broadsword.say("{0.mention}, ooops! Something wrong!".format(self.author))
        finally:
            await asyncio.sleep(1)
            await self.broadsword.delete_message(ctx.message)
            del self.author
            del self.code
            try:
                del self.cnx
                print("del self.cnx")
            except:
                pass
            try:
                del self.auth_roles
                print("del self.auth_roles")
            except:
                pass
            try:
                del self.auth_group
                print("del self.auth_group")
            except:
                pass
            try:
                del self.charname
                print("del self.charname")
            except:
                pass
            try:
                del self.role
                print("del self.role")
            except:
                pass
            try:
                del self.corp_role
                print("del self.corp_role")
            except:
                pass
            try:
                del self.pending
                print("del self.pending")
            except:
                pass
            try:
                del self.corpinfo
                print("del self.corpinfo")
            except:
                pass
            try:
                del self.corpinfo_temp
                print("del self.corpinfo_temp")
            except:
                pass
            try:
                del self.charinfo
                print("del self.charinfo")
            except:
                pass
            try:
                del self.bot_answer
                print("del self.bot_answer")
            except:
                pass

def setup(broadsword):
    broadsword.add_cog(AuthUser(broadsword))