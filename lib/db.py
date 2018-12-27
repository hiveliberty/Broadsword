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

class DB:
    def __init__(self):
        try:
            self.cnx = mysqldb.connect(**dbcfg)
            self.cursor = self.cnx.cursor(dictionary=True)
        except mysqldb.Error:
            log.exception("An exception has occurred in {}: ".format(__name__))

    def __del__(self):
        try:
            self.cursor.close()
            self.cnx.close()
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
            if values is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)

            if config.bot["devMode"]:
                log.info("{}\n".format(self.cursor.statement))

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
            self.cursor.execute(query, values)

            if config.bot["devMode"]:
                log.info("{}\n".format(self.cursor.statement))

            self.cnx.commit()
            return 0
        except mysqldb.Error:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def message_add(self, msg, channel_id):
        self.sqlquery = "INSERT INTO `discord_queue_message` (channel_id, message) VALUES (%s, %s)"
        await self._query_exec(self.sqlquery, (channel_id, msg))
        del self.sqlquery
        return None

    async def message_get(self, id):
        self.sqlquery = "SELECT * FROM `discord_queue_message` WHERE id=%s"
        self.sqlout = await self._query(self.sqlquery, (id,), query_one=True)
        if self.sqlout is not None:
            return self.sqlout
        return None

    async def message_get_oldest(self):
        self.sqlquery = "SELECT MIN(id) FROM `discord_queue_message`"
        self.sqlout = await self._query(self.sqlquery, query_one=True)
        del self.sqlquery
        if self.sqlout is not None:
            return self.sqlout['MIN(id)']
        return None

    async def message_delete(self, id):
        self.sqlquery = "DELETE FROM `discord_queue_message` WHERE id=%s"
        await self._query_exec(self.sqlquery, (id,))
        del self.sqlquery
        return None

    async def message_set_maxprio(self, msg, channel_id):
        self.oldest = await self.message_get_oldest()
        if self.oldest is not None:
            self.id = self.oldest - 1
            self.sqlquery = "INSERT INTO `discord_queue_message` " +\
                            "(id, channel_id, message) " +\
                            "VALUES (%s, %s, %s)"
            await self._query_exec(self.sqlquery, (self.id, channel_id, msg))
        del self.sqlquery
        del self.id
        del self.oldest
        return None

    async def custom_add(self, key, value):
        sql = ("INSERT INTO `custom_storage`"
               " (custom_key, custom_value) VALUES (%s, %s);")
        result = await self._query_exec(sql, (key, value))
        return result

    async def custom_update(self, key, value):
        sql = ("UPDATE `custom_storage`"
               " SET custom_value = %s WHERE custom_key = %s;")
        result = await self._query_exec(sql, (value, key))
        return result

    async def custom_get(self, key):
        sql = ("SELECT custom_value FROM `custom_storage`"
               " WHERE custom_key = %s LIMIT 1;")
        result = await self._query(sql, (key,), True)
        if result is not None:
            return result['custom_value']
        else:
            return None

    async def custom_del(self, key):
        sql = ("DELETE FROM `custom_storage` WHERE custom_key = %s;")
        result = await self._query_exec(sql, (key,))
        return result

    async def token_update(self, id, access_t, scope, expire_date):
        sql = ("UPDATE `esi_tokens` SET access_token = %s, expire_date = %s"
               " WHERE character_id = %s AND scope_name = %s;")
        result = await self._query_exec(sql,
            (access_t, expire_date, id, scope))
        return result

    async def token_updatefull(self, id, access_t, refresh_t, scope, expire_date):
        sql = ("UPDATE `esi_tokens` SET access_token = %s, refresh_token = %s,"
               " expire_date = %s WHERE character_id = %s AND scope_name = %s;")
        result = await self._query_exec(sql,
            (access_t, refresh_t, expire_date, id, scope))
        return result

    async def token_get(self, type, scope):
        id = await self.custom_get(type)
        sql = ("SELECT"
               " character_id, access_token, refresh_token, expire_date, scope_name"
               " FROM `esi_tokens`"
               " WHERE character_id = %s AND scope_name = %s LIMIT 1;")
        result = await self._query(sql, (id, scope), True)
        return result

    # async def authorized_get(self, id):
        # sql = ("SELECT * FROM `discord_users`"
               # " WHERE discord_id = %s LIMIT 1;")
        # result = await self._query(sql, (id,), True)
        # if result is not None:
            # return result['custom_value']
        # else:
            # return None

    async def authorized_exist(self, id):
        sql = ("SELECT * FROM `discord_users`"
               " WHERE discord_id = %s LIMIT 1;")
        result = await self._query(sql, (id,), True)
        if result is not None:
            if result['user_id'] is not None:
                return True
            else:
                return False
        else:
            return False

    async def authorized_del(self, id):
        sql = ("DELETE FROM `discord_users` WHERE discord_id = %s;")
        result = await self._query_exec(sql, (id,))
        return result

    async def member_add(self, id, nickname, bot):
        sql = ("INSERT INTO `discord_members`"
               " (discord_id, discord_username, is_bot) VALUES (%s, %s, %s);")
        result = await self._query_exec(sql, (id, nickname, bot))
        return result

    async def member_exist(self, id):
        sql = ("SELECT * FROM `discord_members`"
               " WHERE discord_id = %s;")
        result = await self._query(sql, (id,), True)
        if result is not None:
            if result['discord_username'] is not None:
                return True
            else:
                return False
        else:
            return False

    async def member_del(self, id):
        sql = ("DELETE FROM `discord_members` WHERE discord_id = %s;")
        result = await self._query_exec(sql, (id,))
        return result


class DBStart(DB):
    def __init__(self):
        super().__init__()

    def __del__(self):
        super().__del__()

    def _query(self, query, values=None, query_one=False):
        try:
            if values is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)

            if config.bot["devMode"]:
                log.info("{}\n".format(self.cursor.statement))

            if query_one:
                out = self.cursor.fetchone()
                return out
            else:
                out = self.cursor.fetchall()
                return out
        except mysqldb.Error:
            log.exception("An exception has occurred in {}: ".format(__name__))

    def _query_exec(self, query, values=None):
        try:
            if values is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, values)

            if config.bot["devMode"]:
                log.info("{}\n".format(self.cursor.statement))

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

    def message_check(self):
        sql = "SELECT * FROM `discord_queue_message`"
        out = self._query(sql)
        if len(out) > 35:
            self.message_clear()
        return None

    def message_clear(self):
        sql = "DELETE from `discord_queue_message`"
        self._query_exec(sql)
        log.info("Cache was cleaned")
        return
