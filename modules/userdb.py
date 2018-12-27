import discord
import asyncio
import logging
from discord.ext import commands as broadsword

from config import config
from lib.db import DBMain
from lib.utils import UserdbUtils

log = logging.getLogger(__name__)


class UserDB:
    """Store joined discord users in DB"""
    def __init__(self, bot):
        self.broadsword = bot

    async def _selfclean(self, vars):
        for attr in vars: self.__dict__.pop(attr,None)

    async def _make_id_list(self):
        self.list = []
        for self.member in self.members:
            self.list.append(self.member["discord_id"])
        return self.list

    async def _member_id_list(self):
        try:
            self.temp_members = await self.cnx.member_select_all()
            await self._make_id_list()
            return self.list
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(("cnx", "members", "member", "list"))

    @broadsword.group(pass_context=True, hidden=False, description='''Группа тестовых команд.''')
    async def userdb(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.broadsword.say("{0.mention}, invalid test command passed...".\
                format(ctx.message.author))

    @userdb.command(pass_context=True, description='''Тестовая команда.''')
    async def test(self, ctx):
        try:
            await self.broadsword.say(str(ctx.message.author))
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(
                ("cnx", "authorized", "members", "member", "user")
            )

    # @userdb.command(pass_context=True, description='''Тестовая команда.''')
    # async def fill(self, ctx):
        # try:
            # self.cnx = DBMain()
            # self.members = await UserdbUtils().member_id_list()
            # self.server = self.broadsword.get_server(id=config.bot["guild"])
            # for self.member in self.server.members:
                # if not self.member.bot:
                    # if self.member.id not in self.members:
                        # log.info("User '{}' added to discord members db.".\
                            # format(self.member)
                        # )
                        # await self.cnx.member_add(self.member.id)

            # self.members = await UserdbUtils().member_id_list()
            # self.authorized = await self.cnx.auth_users_select()
            # for self.user in self.authorized:
                # if self.user["discord_id"] in self.members:
                    # await self.cnx.member_set_authorized(self.user["discord_id"])
        # except Exception:
            # log.exception("An exception has occurred in {}: ".format(__name__))
        # finally:
            # await self._selfclean(
                # ("cnx", "authorized", "members", "member", "user")
            # )

    async def on_member_join(self, member):
        try:
            log.info("User '{}' joined to the server.".format(member))
            self.cnx = DBMain()
            exist = await self.cnx.member_exist(member.id)
            if not exist:
                await self.cnx.member_add(member.id,str(member),member.bot)
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(("cnx"))

    async def on_member_remove(self, member):
        try:
            log.info("User '{}' left the server.".format(member))
            self.cnx = DBMain()
            await self.cnx.authorized_del(member.id)
            await self.cnx.member_del(member.id)
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(("cnx"))


class TaskUserDB:
    def __init__(self, bot):
        self.broadsword = bot
        self._task = self.broadsword.loop.create_task(self.userdb_task())
        log.info("UserDB.Task should have been run.")

    def __unload(self):
        self._task.cancel()
        log.info("UserDB.Task should have been unloaded.")

    async def userdb_task(self):
        try:
            while not self.broadsword.is_closed:
                pass
                await asyncio.sleep(10)
        except asyncio.CancelledError:
            pass
        except (OSError, discord.ConnectionClosed):
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.userdb_task())
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
            self._task.cancel()
            self._task = self.broadsword.loop.create_task(self.message_task())


def setup(broadsword):
    broadsword.add_cog(UserDB(broadsword))
#    broadsword.add_cog(TaskUserDB(broadsword))
