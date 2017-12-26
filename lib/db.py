#============================================================================
#	functions for working with DB
#   
#   Class DBMain is actual for use
#   Class DBStart is actual for use
#
#============================================================================

import asyncio
import logging
import mysql.connector as mysqldb
#from mysql.connector import errorcode

from config import config
from config.config import db as dbcfg

log = logging.getLogger("library.db")
#log = logging.getLogger(__name__)

class DB:
    def __init__(self):
        try:
            self.cnx = mysqldb.connect(**dbcfg)
            self.cursor = self.cnx.cursor(dictionary=True)
            if config.bot["devMode"]:
                log.info("Database connection opened.")
        except mysqldb.Error:
            log.exception("An exception has occurred in {}: ".format(__name__))

    def __del__(self):
        try:
            self.cursor.close()
            if config.bot["devMode"]:
                log.info("Cursor closed.")
            self.cnx.close()
            if config.bot["devMode"]:
                log.info("Database connection closed.")
        except mysqldb.Error:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("cnx", "cursor"):
                self.__dict__.pop(attr,None)
            del self


class DBMain(DB):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    async def _query(self, query, values=None, query_one=False):
        try:
            #if config.bot["devMode"]:
            #    log.info("{}\n".format(query))
            if values is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)
            if query_one:
                self.sqlout = self.cursor.fetchone()
                return self.sqlout
            else:
                self.sqlout = self.cursor.fetchall()
                return self.sqlout
        except mysqldb.Error:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def _query_exec(self, query, values):
        try:
            #if config.bot["devMode"]:
            #    log.info("{}\n".format(query))
            self.cursor.execute(query, values)
            self.cnx.commit()
            return 0
        except mysqldb.Error:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def discord_add_user(self, discord_id):
        self.sqlquery = "REPLACE INTO `discord_users_cache` SET discord_id=%s"
        #self.sqlquery = "INSERT INTO `discordUsers` SET discord_id='{0}'".format(discord_id)
        #self.sqlquery = "REPLACE INTO `discordUsers` (discord_id, is_authorized) VALUES ('{0}', 'no')".format(discord_id)
        await self._query_exec(self.sqlquery, (discord_id,))
        del self.sqlquery
        return None

    async def discord_set_authorized(self, discord_id):
        self.sqlquery = "UPDATE `discord_users_cache` SET is_authorized='yes' WHERE discord_id=%s"
        await self._query_exec(self.sqlquery, (discord_id,))
        del self.sqlquery
        return None

    async def discord_set_unauthorized(self, discord_id):
        self.sqlquery = "UPDATE `discord_users_cache` SET is_authorized='no' WHERE discord_id=%s"
        await self._query_exec(self.sqlquery, (discord_id,))
        del self.sqlquery
        return None

    async def discord_delete_user(self, discord_id):
        self.sqlquery = "DELETE FROM `discord_users_cache` WHERE discord_id=%s"
        await self._query_exec(self.sqlquery, (discord_id,))
        del self.sqlquery
        return None

    async def insert_user(self, character_id, discord_id, eve_name):
        self.sqlquery = "REPLACE INTO `discord_users_auth` " +\
                        "(character_id, discord_id, eve_name, active) " +\
                        "VALUES (%s, %s, %s, 'yes')"
        await self._query_exec(self.sqlquery, (character_id, discord_id, eve_name))
        del self.sqlquery
        return None

    async def auth_enabled(self, character_id):
        self.sqlquery = "UPDATE `discord_users_auth` SET pending='yes' WHERE character_id=%s"
        await self._query_exec(self.sqlquery, (character_id,))
        del self.sqlquery
        return None

    async def auth_disable(self, character_id):
        self.sqlquery = "UPDATE `discord_users_auth` SET pending='no' WHERE character_id=%s"
        await self._query_exec(self.sqlquery, (character_id,))
        del self.sqlquery
        return None

    async def user_enabled(self, character_id):
        self.sqlquery = "UPDATE `discord_users_auth` SET active='yes' WHERE character_id=%s"
        await self._query_exec(self.sqlquery, (character_id,))
        del self.sqlquery
        return None

    async def user_update(self, character_id, key, value):
        self.sqlquery = "UPDATE `discord_users_auth` " +\
                        "SET {}=%s WHERE character_id=%s".format(key)
        await self._query_exec(self.sqlquery, (value, character_id))
        del self.sqlquery
        return None

    async def user_disable(self, character_id):
        self.sqlquery = "UPDATE `discord_users_auth` SET active='no' WHERE character_id=%s"
        await self._query_exec(self.sqlquery, (character_id,))
        del self.sqlquery
        return None

    async def select_pending(self):
        self.sqlquery = "SELECT * " +\
                        "FROM `discord_users_auth` " +\
                        "WHERE pending='yes'"
        self.sqlout = await self._query(self.sqlquery, query_one=True)
        del self.sqlquery
        if self.sqlout is not None:
            return self.sqlout
        return None

    async def select_users(self):
        self.sqlquery = "SELECT discord_id, character_id, eve_name " +\
                        "FROM `discord_users_auth` " +\
                        "WHERE active='yes' AND pending='no'"
        self.sqlout = await self._query(self.sqlquery)
        del self.sqlquery
        if self.sqlout is not None:
            return self.sqlout
        return None

    async def message_add(self, msg, channel_id):
        self.sqlquery = "INSERT INTO `queue_message` (channel_id, message) VALUES (%s, %s)"
        await self._query_exec(self.sqlquery, (channel_id, msg))
        del self.sqlquery
        return None

    async def message_get(self, id):
        self.sqlquery = "SELECT * FROM `queue_message` WHERE id=%s"
        self.sqlout = await self._query(self.sqlquery, (id,), query_one=True)
        if self.sqlout is not None:
            return self.sqlout
        return None

    async def message_get_oldest(self):
        self.sqlquery = "SELECT MIN(id) FROM `queue_message`"
        self.sqlout = await self._query(self.sqlquery, query_one=True)
        del self.sqlquery
        if self.sqlout is not None:
            return self.sqlout['MIN(id)']
        return None

    async def message_delete(self, id):
        self.sqlquery = "DELETE FROM `queue_message` WHERE id=%s"
        await self._query_exec(self.sqlquery, (id,))
        del self.sqlquery
        return None

    async def message_set_maxprio(self, msg, channel_id):
        self.oldest = await self.message_get_oldest()
        if self.oldest is not None:
            self.id = self.oldest - 1
            self.sqlquery = "INSERT INTO `queue_message` " +\
                            "(id, channel_id, message) " +\
                            "VALUES (%s, %s, %s)"
            await self._query_exec(self.sqlquery, (self.id, channel_id, msg))
        del self.sqlquery
        del self.id
        del self.oldest
        return None

    async def rename_add(self, discord_id, nick):
        self.sqlquery = "INSERT INTO `queue_rename` " +\
                        "(discord_id, nick) " +\
                        "VALUES (%s, %s)"
        await self._query_exec(self.sqlquery, (discord_id, nick))
        del self.sqlquery
        return None

    async def rename_get(self, id):
        self.sqlquery = "SELECT * FROM `queue_rename` WHERE id=%s"
        self.sqlout = await self._query(self.sqlquery, (id,), True)
        del self.sqlquery
        if self.sqlout is not None:
            return self.sqlout
        return None

    async def rename_get_oldest(self):
        self.sqlquery = "SELECT MIN(id) FROM `queue_rename`"
        self.sqlout = await self._query(self.sqlquery, query_one=True)
        del self.sqlquery
        if self.sqlout is not None:
            return self.sqlout['MIN(id)']
        return None

    async def rename_delete(self, id):
        self.sqlquery = "DELETE FROM `queue_rename` WHERE id=%s"
        await self._query_exec(self.sqlquery, (id,))
        del self.sqlquery
        return None

    async def corpinfo_add(self, corporation_id, corporation_ticker, corporation_name, corporation_role):
        self.sqlquery = "REPLACE INTO `corporation_cache` " +\
                        "(corporation_id, corporation_ticker, corporation_name, corporation_role) " +\
                        "VALUES ('{0}', '{1}', '{2}', '{3}')"
        await self._query_exec(
            self.sqlquery,
            (corporation_id, corporation_ticker,
             corporation_name, corporation_role)
        )
        del self.sqlquery
        return None
        
    async def corpinfo_update(self, corporation_id, key, value):
        self.sqlquery = "UPDATE `corporation_cache` " +\
                        "SET %s=%s WHERE corporation_id=%s"
        await self._query_exec(self.sqlquery, (key, value, corporation_id))
        del self.sqlquery
        return None

    async def corpinfo_get(self, corporation_id):
        self.sqlquery = "SELECT * FROM `corporation_cache` " +\
                        "WHERE corporation_id=%s"
        self.sqlout = await self._query(self.sqlquery, (corporation_id,), True)
        del self.sqlquery
        if self.sqlout is not None:
            return self.sqlout
        return None

    async def corpinfo_delete(self, corporation_id):
        self.sqlquery = "DELETE FROM `corporation_cache` " +\
                        "WHERE corporation_id=%s"
        await self._query_exec(self.sqlquery)
        del self.sqlquery
        return None

    async def storage_add(self, key, value):
        self.sqlquery = "REPLACE INTO `storage` " +\
                        "(`s_key`, `s_value`) VALUES (%s, %s)"
        await self._query_exec(self.sqlquery, (key, value))
        del self.sqlquery
        return None

    async def storage_update(self, key, value):
        self.sqlquery = "UPDATE `storage` SET s_value=%s WHERE s_key=%s"
        await self._query_exec(self.sqlquery, (value, key))
        del self.sqlquery
        return None

    async def storage_get(self, key):
        self.sqlquery = "SELECT s_value FROM `storage` WHERE `s_key`=%s"
        self.sqlout = await self._query(self.sqlquery, (key,), True)
        del self.sqlquery
        if self.sqlout is not None:
            return self.sqlout["s_value"]
        return None

    async def storage_delete(self, key):
        self.sqlquery = "DELETE FROM `storage` WHERE `s_key`=%s"
        await self._query_exec(self.sqlquery, (key,))
        del self.sqlquery
        return None

    async def token_get(self, character_id):
        self.sqlquery = "SELECT * FROM `token_storage` WHERE `character_id`=%s"
        self.sqlout = await self._query(self.sqlquery, (character_id,), True)
        del self.sqlquery
        if self.sqlout is not None:
            return self.sqlout
        return None

    async def token_update(self, character_id, token_access, token_refresh, updated):
        self.sqlquery = "REPLACE INTO `token_storage` " +\
                        "(`character_id`, `token_access`, `token_refresh`, `updated`) " +\
                        "VALUES (%s, %s, %s, %s)"
        await self._query_exec(
            self.sqlquery,
            (character_id, token_access, token_refresh, updated)
        )
        del self.sqlquery
        return None

    async def token_delete(self, character_id):
        self.sqlquery = "DELETE FROM `token_storage` " +\
                        "WHERE `character_id`=%s"
        await self._query_exec(self.sqlquery, (character_id,))
        del self.sqlquery
        return None

        
class DBStart(DB):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def _query(self, query, values=None, query_one=False):
        try:
            #if config.bot["devMode"]:
            #    log.info("{}\n".format(query))
            if values is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)
            if query_one:
                self.sqlout = self.cursor.fetchone()
                return self.sqlout
            else:
                self.sqlout = self.cursor.fetchall()
                return self.sqlout
        except mysqldb.Error:
            log.exception("An exception has occurred in {}: ".format(__name__))

    def _query_exec(self, query, values):
        try:
            #if config.bot["devMode"]:
            #    log.info("{}\n".format(query))
            self.cursor.execute(query, values)
            self.cnx.commit()
            return 0
        except mysqldb.Error:
            log.exception("An exception has occurred in {}: ".format(__name__))

    def mysql_version(self):
        self.sqlquery = "SELECT version()"
        self.sqlout = self._query(self.sqlquery)
        if self.sqlout is not None:
            return self.sqlout[0]['version()']
        return None

    def db_version(self):
        self.sqlquery = "SELECT version()"
        self.sqlout = self._query(self.sqlquery)
        if self.sqlout is not None:
            return self.sqlout[0]['version()']
        return None

    def storage_add(self, key, value):
        self.sqlquery = "REPLACE INTO `storage` " +\
                        "(`s_key`, `s_value`) VALUES (%s, %s)"
        self._query_exec(self.sqlquery, (key, value))
        del self.sqlquery
        return None

    def storage_update(self, key, value):
        self.sqlquery = "UPDATE `storage` SET s_value=%s WHERE s_key=%s"
        self._query_exec(self.sqlquery, (value, key))
        del self.sqlquery
        return None

    def storage_get(self, key):
        self.sqlquery = "SELECT s_value FROM `storage` WHERE `s_key`=%s"
        self.sqlout = self._query(self.sqlquery, (key,), True)
        del self.sqlquery
        #if len(self.sqlout) >= 1:
        #    return self.sqlout[0]['s_value']
        if self.sqlout is not None:
            return self.sqlout
        return None

    def message_check(self):
        self.sqlquery = "SELECT * FROM `queue_message`"
        self.sqlout = self._query(self.sqlquery)
        del self.sqlquery
        if len(self.sqlout) > 35:
            self.clearMessageQueue()
        return None

    def message_clear(self):
        self.sqlquery = "DELETE from `queue_message`"
        self._query_exec(self.sqlquery)
        if config.bot["devMode"]:
            print("Cache was cleaned")
        else:
            log.info("Cache was cleaned")
        del self.sqlquery
        return None
