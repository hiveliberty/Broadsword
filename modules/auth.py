import sys
import asyncio
import weakref
import json
import discord
import logging
from importlib import reload
from discord.ext import commands as broadsword
from lib.eve import EVEApi
from lib.db import DBMain
from lib.utils import AuthUtils
from config import config

log = logging.getLogger(__name__)

class AuthCMD:
    def __init__(self, bot):
        self.broadsword = bot
        self.eveapi = EVEApi()
        self.server = self.broadsword.get_server(id=config.bot["guild"])

    @broadsword.group(pass_context=True, hidden=False)
    #@broadsword.group(pass_context=True, hidden=False, description='''Группа команд администратора.''')
    async def authadmin(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say(  
                "{0.mention}, invalid git command passed...".format(self.author)
            )

    @authadmin.command(pass_context=True)
    async def reloadconf(self, ctx):
        try:
            reload(config)
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))


class AuthCheck:
    def __init__(self, bot):
        self.broadsword = bot
        self.server = self.broadsword.get_server(id=config.bot["guild"])
        self.eveapi = EVEApi()
        self.interval = config.auth["periodicCheckInterval"]
        self._task = self.broadsword.loop.create_task(self.auth_check())
        self.msg_start = "{} should have been run.".\
            format(__class__.__name__)
        self.msg_stop = "{} should have been unloaded.".\
            format(__class__.__name__)
        if config.bot["devMode"]:
            print(self.msg_start)
        else:
            log.info(self.msg_start)
        
    def __unload(self):
        self._task.cancel()
        if config.bot["devMode"]:
            print(self.msg_stop)
        else:
            log.info(self.msg_stop)

    async def auth_check(self):
        try:
            while not self.broadsword.is_closed:
                if config.bot["devMode"]:
                    print("Start periodic check authorization.")
                else:
                    log.info("Start periodic check authorization.")
                self.auth_groups = await AuthUtils().get_auth_group_ids()
                self.cnx = DBMain()
                self.auth_users = await self.cnx.select_users()
                for self.auth_user in self.auth_users:
                    self.member = self.server.get_member(
                                    self.auth_user["discordID"])
                    if self.member == self.server.owner:
                        continue
                    self.is_exempt = await AuthUtils().is_auth_exempt(
                                            self.member.roles)
                    if not self.is_exempt:
                        self.charinfo = await self.eveapi.char_get_details(
                                                self.auth_user["characterID"])
                        if self.charinfo is not None:
                            if str(self.charinfo["alliance_id"]) not in self.auth_groups:
                                await self.cnx.user_disable(
                                    self.auth_user["characterID"]
                                )
                                await self.broadsword.remove_roles(
                                    self.member,
                                    *self.member.roles
                                )
                                if config.auth["kickWhenLeaving"]:
                                    await self.broadsword.kick(self.member)
                                else:
                                    await self.cnx.discord_set_unauthorized(
                                        self.auth_user["discordID"]
                                    )
                                #if config.auth["alertChannel"] is not None or config.auth["alertChannel"] != "":
                                if config.auth["alertChannel"] != "":
                                    self.channel = self.broadsword.get_channel(
                                        config.auth["alertChannel"]
                                    )
                                    await self.broadsword.send_message(
                                        self.channel,
                                        "{} left corp\\alliance.".\
                                            format(self.auth_user["eveName"])
                                    )
                                else:
                                    await self.broadsword.send_message(
                                        self.server.owner,
                                        "Warning! alertChannel is not set!"
                                    )
                        else:
                            if config.bot["devMode"]:
                                print("EVE services temprorary unavailable!")
                            else:
                                log.warning("EVE services temprorary unavailable!")
                del self.cnx
                await asyncio.sleep(self.interval)
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.auth_check())
        except asyncio.CancelledError as ec:
            if config.bot["devMode"]:
                print(ec)
            log.exception("asyncio.CancelledError: ")
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.auth_check())


class AuthTask:
    def __init__(self, bot):
        self.broadsword = bot
        self.server = self.broadsword.get_server(id=config.bot["guild"])
        self.eveapi = EVEApi()
        self.interval = 3
        self._task = self.broadsword.loop.create_task(self.auth_task())
        self.msg_start = "{} should have been run.".\
            format(__class__.__name__)
        self.msg_stop = "{} should have been unloaded.".\
            format(__class__.__name__)
        if config.bot["devMode"]:
            print(self.msg_start)
        else:
            log.info(self.msg_start)
        
    def __unload(self):
        self._task.cancel()
        if config.bot["devMode"]:
            print(self.msg_stop)
        else:
            log.info(self.msg_stop)

    async def auth_task(self):
        try:
            while not self.broadsword.is_closed:
                log.info("Start periodic check for new authorizations.")
                #print("Start periodic check for new authorizations..")
                self.cnx = DBMain()

                self.pending = await self.cnx.select_pending()
                #   self.pendings content:
                #      `id` int(11) NOT NULL AUTO_INCREMENT,
                #      `eveName` varchar(365) DEFAULT NULL,
                #      `characterID` varchar(128) NOT NULL,
                #      `corporationID` varchar(128) NOT NULL,
                #      `allianceID` varchar(128) NOT NULL,
                #      `discordID` varchar(64) NOT NULL,
                #      `active` varchar(10) NOT NULL,
                #      `pending` varchar(10) NOT NULL,
                #      `addedOn` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

                if self.pending is not None:
                    await self.auth(self.pending)
                    log.info("{} has been authorized.".format(self.pending["eveName"]))
                else:
                    log.info("There is no one to authorize.")
                    #print("There is no one to authorize..")
                for attr in ("cnx", "pending"):
                    self.__dict__.pop(attr,None)
                await asyncio.sleep(self.interval)
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.auth_task())
        except asyncio.CancelledError as ec:
            if config.bot["devMode"]:
                print(ec)
            log.exception("asyncio.CancelledError: ")
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.auth_task())
        finally:
            for attr in ("cnx", "pending"):
                self.__dict__.pop(attr,None)

    async def auth(self, pending):
        try:
            while not self.broadsword.is_closed:
                self.cnx = DBMain()

                self.pending = pending
                #   self.pendings content:
                #      `id` int(11) NOT NULL AUTO_INCREMENT,
                #      `eveName` varchar(365) DEFAULT NULL,
                #      `characterID` varchar(128) NOT NULL,
                #      `corporationID` varchar(128) NOT NULL,
                #      `allianceID` varchar(128) NOT NULL,
                #      `discordID` varchar(64) NOT NULL,
                #      `active` varchar(10) NOT NULL,
                #      `pending` varchar(10) NOT NULL,
                #      `addedOn` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

                self.auth_roles = []
                self.not_member = True
                self.do_authorize = False
                self.member = self.server.get_member(self.pending["discordID"])

                for self.role in self.member.roles:
                    self.auth_roles.append(self.role)

                self.auth_groups = await AuthUtils().get_auth_group_ids()
                if self.pending["allianceID"] in self.auth_groups:
                    self.auth_group = await AuthUtils().get_auth_group_values(self.pending["allianceID"])

                    self.corpinfo = await self.cnx.corpinfo_get(self.pending["corporationID"])
                    #self.corpinfo._parent = weakref.ref(self)
                    #   self.corpinfo content:
                    #      `id` int(11) NOT NULL AUTO_INCREMENT,
                    #      `corpID` varchar(128) NOT NULL,
                    #      `allianceID` varchar(128) DEFAULT NULL,
                    #      `corpTicker` varchar(10) NOT NULL,
                    #      `corpName` varchar(255) NOT NULL,
                    #      `corpRole` varchar(255) NOT NULL,

                    if self.corpinfo is None:
                        self.corpinfo = {}
                        self.temp = await self.eveapi.corp_get_details(self.pending["corporationID"])
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
                        if self.temp is None:
                            continue
                        self.corpinfo["corpTicker"] = self.temp["ticker"]
                        self.corpinfo["corpName"] = self.temp["corporation_name"]
                        if self.auth_group["setCorpRole"] and self.auth_group["type"] == "alliance":
                            self.corpinfo["corpRole"] = self.corpinfo["corpTicker"] + " Members"
                            #print("Corp role is '{}'".format(self.corpinfo["corpRole"]))
                        else:
                            self.corpinfo["corpRole"] = ""
                            #print("Corp role is ''")
                        await self.cnx.corpinfo_add(
                            self.pending["corporationID"],
                            self.corpinfo["corpTicker"],
                            self.corpinfo["corpName"],
                            self.corpinfo["corpRole"]
                        )

                    # Update DB if setCorpRole has been enabled
                    if self.corpinfo["corpRole"] == ""\
                    and self.auth_group["setCorpRole"]\
                    and self.auth_group["type"] == "alliance":
                        self.corpinfo["corpRole"] = \
                            self.corpinfo["corpTicker"] + " Members"
                        await self.cnx.corpinfo_update(
                            self.corpinfo["corpID"],
                            "corpRole",
                            self.corpinfo["corpRole"]
                        )

                    if self.auth_group["setCorpRole"]\
                    and self.auth_group["type"] == "alliance":
                        self.role_exist = False
                        self.role = None
                        for self.role in self.server.roles:
                            if self.role.name == self.corpinfo["corpRole"]:
                                self.role_exist = True
                                self.corp_role = self.role
                                break
                        if not self.role_exist:
                            self.corp_role = await self.broadsword.create_role(
                                self.server,
                                name=self.corpinfo["corpRole"],
                                permissions=discord.Permissions(104324160),
                                colour=discord.Colour(self.auth_group["corpColour"]),
                                hoist=True,
                                mentionable=True
                            )
                        if self.corp_role not in self.auth_roles:
                            self.auth_roles.append(self.corp_role)

                    self.role = None
                    for self.role in self.server.roles:
                        if self.role.name == self.auth_group["memberRole"]:
                            if self.role not in self.auth_roles:
                                self.auth_roles.append(self.role)
                                self.do_authorize = True
                                break
                            else:
                                self.do_authorize = True
                                break

                    if self.do_authorize:
                        await self.broadsword.add_roles(self.member, *self.auth_roles)
                        if config.auth["nameEnforce"]:
                            self.charname = ""
                            self.charinfo = await self.eveapi.char_get_details(self.pending["characterID"])
                            if self.auth_group["corpTickers"] and self.auth_group["type"] == "alliance":
                                self.charname = "[" + self.corpinfo["corpTicker"] + "] "
                            self.charname = self.charname + self.charinfo["name"]
                            await self.cnx.rename_add(self.member.id, self.charname)
                        await self.cnx.auth_disable(self.pending["characterID"])
                        await self.cnx.user_enabled(self.pending["characterID"])
                        await self.cnx.user_update(
                            self.pending["characterID"],
                            "eveName",
                            self.charinfo["name"]
                        )
                        await self.cnx.discord_set_authorized(self.member.id)
                        #await self.broadsword.say("{0.mention}, you have been authorized!".format(self.member))
                    #else:
                    #    await self.broadsword.say("{0.mention}, you cann't be authorized, because no role is set for auth!".format(self.member))
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("cnx", "pending", "auth_roles", "member",
                         "auth_groups", "auth_group", "corpinfo",
                         "temp", "role", "corp_role", "do_authorize",
                         "charinfo", "charname"):
                self.__dict__.pop(attr,None)


def setup(broadsword):
    broadsword.add_cog(AuthCMD(broadsword))
    broadsword.add_cog(AuthTask(broadsword))
    if config.auth["periodicCheck"]:
        broadsword.add_cog(AuthCheck(broadsword))
