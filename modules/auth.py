import sys
import asyncio
import weakref
import json
import discord
from importlib import reload
from discord.ext import commands as broadsword
from lib.libeve import EVEApi
from lib.libdb import DB
from lib.utils import AuthUtils
from config import config

class AuthUser:    
    def __init__(self, bot):
        self.broadsword = bot
        self.eveapi = EVEApi()
        self.server = self.broadsword.get_server(id=config.bot["guild"])

    @broadsword.group(pass_context=True, hidden=False, description='''Группа команд администратора.''')
    async def authadmin(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say("{0.mention}, invalid git command passed...".format(self.author))

    @authadmin.command(pass_context=True)
    async def reloadconf(self, ctx):
        try:
            reload(config)
        except Exception as e:
            print(e)
            await self.broadsword.say("Oooops")

    @authadmin.command(pass_context=True, description='''Тестовая команда добавления пользователя для авторизации.''')
    async def addtestuser(self, ctx):
        self.testCharID = ""
        self.testCorpID = ""
        self.testAllianceID = ""
        self.testAuthString = ""
        self.testActive = "1"
        try:
            self.cnx = DB()
            await self.cnx.insertTestUser(self.testCharID, self.testCorpID, self.testAllianceID, self.testAuthString, self.testActive)
            await self.broadsword.say("```User added.```")
        except:
            await self.broadsword.say("Oooops")
        else:
            del self.cnx

    @authadmin.command(pass_context=True, description='''Тестовая команда добавления в очередь сообщений.''')
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

    @authadmin.command(pass_context=True, description='''Тестовая команда добавления в очередь переименования.''')
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

    @authadmin.command(pass_context=True, description='''Команда для тестирования.''')
    async def test(self, ctx):
        try:
            #if config.auth["alertChannel"] is not None or config.auth["alertChannel"] != "":
            #if config.auth["alertChannel"] != "":
                await self.broadsword.send_message(self.server.owner, "Warning! alertChannel is not set!")
        except Exception as e:
            print(e)
            await self.broadsword.say("Oooops")

    @broadsword.command(pass_context=True, description='''Это команда авторизации.''')
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
                self.auth_group_ids = await AuthUtils().get_auth_group_ids()
                if self.pending["allianceID"] in self.auth_group_ids:
                    self.not_member = False
                #if str(self.charinfo["alliance_id"]) not in self.auth_group_ids:
                #for self.group_key, self.group_value in config.auth["authGroups"].items():
                #    if self.group_value["id"] == self.pending["allianceID"]:
                #        self.not_member = False
                #        self.auth_group = self.group_value
                #        del self.group_value
                #        break
                if self.not_member:
                    await self.broadsword.say("{0.mention}, you are not alliance member!".format(self.author))
                    return

                self.auth_group = await AuthUtils().get_auth_group_values()

                self.corpinfo = await self.cnx.getCorpInfo(self.pending["corporationID"])
                #self.corpinfo._parent = weakref.ref(self)
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
                    if self.auth_group["setCorpRole"] and self.auth_group["type"] == "alliance":
                        self.corpinfo["corpRole"] = self.corpinfo["corpTicker"] + " Members"
                        print("Corp role is '{}'".format(self.corpinfo["corpRole"]))
                    else:
                        self.corpinfo["corpRole"] = ""
                        print("Corp role is ''")
                    await self.cnx.addCorpInfo(self.pending["corporationID"], self.corpinfo["corpTicker"], self.corpinfo["corpName"], self.corpinfo["corpRole"])

                #if (self.corpinfo["corpRole"] is None or self.corpinfo["corpRole"] == "") and config.auth["setCorpRole"] and self.auth_group["type"] == "alliance":
                if self.corpinfo["corpRole"] == "" and self.auth_group["setCorpRole"] and self.auth_group["type"] == "alliance":
                    print("setCorpRole has been enabled")
                    self.corpinfo["corpRole"] = self.corpinfo["corpTicker"] + " Members"
                    await self.cnx.addCorpInfo(self.corpinfo["corpID"], self.corpinfo["corpTicker"], self.corpinfo["corpName"], self.corpinfo["corpRole"])

                if self.auth_group["setCorpRole"] and self.auth_group["type"] == "alliance":
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
                            colour=discord.Colour(self.auth_group["corpColour"]),
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
                    await self.cnx.setAuthorized(self.author.id)
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

class AuthTask:
    def __init__(self, bot):
        self.broadsword = bot
        self.server = self.broadsword.get_server(id=config.bot["guild"])
        self.eveapi = EVEApi()
        self.interval = config.auth["periodicCheckInterval"]
        self._task = self.broadsword.loop.create_task(self.qAuthTask())
        print('qAuthTask should have been run in background..')
        
    def __unload(self):
        self._task.cancel()
        print('qAuthTask should have been unloaded..')
        
    async def qAuthTask(self):
        try:
            while not self.broadsword.is_closed:
                print("Start periodic check authorization..")
                self.auth_group_ids = await AuthUtils().get_auth_group_ids()
                self.cnx = DB()
                self.auth_users = await self.cnx.selectUsers()
                for self.auth_user in self.auth_users:
                    self.member = self.server.get_member(self.auth_user["discordID"])
                    if self.member == self.server.owner:
                        print("is owner!")
                        continue
                    self.is_exempt = await AuthUtils().is_auth_exempt(self.member.roles)
                    if not self.is_exempt:
                        self.charinfo = await self.eveapi.getCharDetails(self.auth_user["characterID"])
                        if self.charinfo is not None:
                            if str(self.charinfo["alliance_id"]) not in self.auth_group_ids:
                                await self.cnx.disableUser(self.auth_user["characterID"])
                                await self.broadsword.remove_roles(self.member, *self.member.roles)
                                if config.auth["kickWhenLeaving"]:
                                    await self.broadsword.kick(self.member)
                                else:
                                    await self.cnx.setUnauthorized(self.auth_user["discordID"])
                                #if config.auth["alertChannel"] is not None or config.auth["alertChannel"] != "":
                                if config.auth["alertChannel"] != "":
                                    self.channel = self.broadsword.get_channel(config.auth["alertChannel"])
                                    await self.broadsword.send_message(self.channel, "{} left corp\\alliance.".format(self.auth_user["eveName"]))
                                else:
                                    await self.broadsword.send_message(self.server.owner, "Warning! alertChannel is not set!")
                        else:
                            print("EVE services temprorary unavailable")
                del self.cnx
                await asyncio.sleep(self.interval)
        except Exception as e:
            print(e)
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.qAuthTask())
        except asyncio.CancelledError as e:
            print(e)
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.qAuthTask())

def setup(broadsword):
    broadsword.add_cog(AuthUser(broadsword))
    if config.auth["periodicCheck"]:
        broadsword.add_cog(AuthTask(broadsword))