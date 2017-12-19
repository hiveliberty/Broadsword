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
                print('Database connection opened')
        except mysqldb.Error as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
            if config.bot["devMode"]:
                print('ERROR: %d: %s' % (e.args[0], e.args[1]))

    def __del__(self):
        try:
            self.cursor.close()
            if config.bot["devMode"]:
                print('Cursor closed')
            self.cnx.close()
            if config.bot["devMode"]:
                print('Database connection closed')
        except mysqldb.Error as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
            if config.bot["devMode"]:
                print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            for attr in ("cnx", "cursor"):
                self.__dict__.pop(attr,None)
            del self


class DBMain(DB):
    async def sql_query(self, query):
        try:
            self.cursor.execute(query)
            self.sqlout = self.cursor.fetchall()
            return self.sqlout
        except mysqldb.Error as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
            if config.bot["devMode"]:
                print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            if config.bot["devMode"]:
                print("{}\n".format(query))

    async def sql_query_one(self, query):
        try:
            self.cursor.execute(query)
            self.sqlout = self.cursor.fetchone()
            return self.sqlout
        except mysqldb.Error as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
            if config.bot["devMode"]:
                print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            if config.bot["devMode"]:
                print("{}\n".format(query))

    async def sql_query_exec(self, query):
        try:
            self.cursor.execute(query)
            self.cnx.commit()
            return 0
        except mysqldb.Error as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
            if config.bot["devMode"]:
                print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            if config.bot["devMode"]:
                print("{}\n".format(query))

    async def discord_add_user(self, discord_id):
        self.sqlquery = "REPLACE INTO `discord_users_cache` SET discord_id='{0}'".format(discord_id)
        #self.sqlquery = "INSERT INTO `discordUsers` SET discord_id='{0}'".format(discord_id)
        #self.sqlquery = "REPLACE INTO `discordUsers` (discord_id, is_authorized) VALUES ('{0}', 'no')".format(discord_id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def discord_set_authorized(self, discord_id):
        self.sqlquery = "UPDATE `discord_users_cache` SET is_authorized='yes' WHERE discord_id='{}'".format(discord_id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def discord_set_unauthorized(self, discord_id):
        self.sqlquery = "UPDATE `discord_users_cache` SET is_authorized='no' WHERE discord_id='{}'".format(discord_id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def discord_delete_user(self, discord_id):
        self.sqlquery = "DELETE FROM `discord_users_cache` WHERE discord_id='{}'".format(discord_id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def insert_user(self, character_id, discord_id, eve_name):
        self.sqlquery = """
                        REPLACE INTO `discord_users_auth`
                        (character_id, discord_id, eve_name, active)
                        VALUES ('{0}','{1}','{2}','yes')
                        """.format(character_id, discord_id, eve_name)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def auth_enabled(self, character_id):
        self.sqlquery = "UPDATE `discord_users_auth` SET pending='yes' WHERE character_id='{}'".format(character_id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def auth_disable(self, character_id):
        self.sqlquery = "UPDATE `discord_users_auth` SET pending='no' WHERE character_id='{}'".format(character_id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def user_enabled(self, character_id):
        self.sqlquery = "UPDATE `discord_users_auth` SET active='yes' WHERE character_id='{}'".format(character_id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def user_update(self, character_id, key, value):
        self.sqlquery = "UPDATE `discord_users_auth` SET {1}='{2}' WHERE character_id='{0}'".format(character_id, key, value)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def user_disable(self, character_id):
        self.sqlquery = "UPDATE `discord_users_auth` SET active='no' WHERE character_id='{}'".format(character_id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def select_pending(self):
        self.sqlquery = """SELECT *
                           FROM `discord_users_auth`
                           WHERE pending='yes'"""
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]
        return None

    async def select_users(self):
        self.sqlquery = """SELECT discord_id, character_id, eve_name
                           FROM `discord_users_auth`
                           WHERE active='yes' AND pending='no'"""
        self.sqlout = await self.sql_query(self.sqlquery)
        return self.sqlout

    async def message_add(self, msg, channel_id):
        self.sqlquery = "INSERT INTO `queue_message` (message, channel_id) VALUES ('{0}', '{1}')".format(msg, channel_id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def message_get(self, id):
        self.sqlquery = "SELECT * FROM `queue_message` WHERE id='{}'".format(id)
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]
        return None

    async def message_get_oldest(self):
        self.sqlquery = "SELECT MIN(id) FROM `queue_message`"
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]['MIN(id)']
        return None

    async def message_delete(self, id):
        self.sqlquery = "DELETE FROM `queue_message` WHERE id='{}'".format(id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def message_set_maxprio(self, msg, channel_id):
        self.oldest = await self.message_get_oldest()
        if self.oldest is not None:
            self.sqlquery = """
                            INSERT INTO `queue_message`
                            (id, message, channel_id)
                            VALUES ('{0}', '{1}', '{2}')
                            """.format(self.id, msg, channel_id)
            await self.sql_query_exec(self.sqlquery)
        return None

    async def rename_add(self, discord_id, nick):
        self.sqlquery = "INSERT INTO `queue_rename` (discord_id, nick) VALUES ('{0}', '{1}')".format(discord_id, nick)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def rename_get(self, id):
        self.sqlquery = "SELECT * FROM `queue_rename` WHERE id='{}'".format(id)
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]
        return None

    async def rename_get_oldest(self):
        self.sqlquery = "SELECT MIN(id) FROM `queue_rename`"
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]['MIN(id)']
        return None

    async def rename_delete(self, id):
        self.sqlquery = "DELETE FROM `queue_rename` WHERE id='{}'".format(id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def corpinfo_add(self, corporation_id, corporation_ticker, corporation_name, corporation_role):
        self.sqlquery = """
                        REPLACE INTO `corporation_cache`
                        (corporation_id, corporation_ticker, corporation_name, corporation_role)
                        VALUES ('{0}', '{1}', '{2}', '{3}')
                        """.format(corporation_id, corporation_ticker, corporation_name, corporation_role)
        await self.sql_query_exec(self.sqlquery)
        return None
        
    async def corpinfo_update(self, corporation_id, key, value):
        self.sqlquery = "UPDATE `corporation_cache` SET {1}='{2}' WHERE corporation_id='{0}'".format(corporation_id, key, value)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def corpinfo_get(self, corporation_id):
        self.sqlquery = "SELECT * FROM `corporation_cache` WHERE corporation_id='{}'".format(corporation_id)
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) == 0:
            return
        return self.sqlout[0]

    async def corpinfo_delete(self, corporation_id):
        self.sqlquery = "DELETE FROM `corporation_cache` WHERE corporation_id='{}'".format(corporation_id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def storage_add(self, key, value):
        self.sqlquery = "REPLACE INTO `storage` (`s_key`, `s_value`) VALUES ('{0}', '{1}')".format(key, value)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def storage_update(self, key, value):
        self.sqlquery = "UPDATE `storage` SET s_value='{1}' WHERE s_key='{0}'".format(key, value)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def storage_get(self, key):
        self.sqlquery = "SELECT s_value FROM `storage` WHERE `s_key`='{}'".format(key)
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]['s_value']
        return None

    async def storage_delete(self, key):
        self.sqlquery = "DELETE FROM `storage` WHERE `s_key`='{}'".format(key)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def token_get(self, character_id):
        self.sqlquery = "SELECT * FROM `token_storage` WHERE `character_id`='{}'".format(character_id)
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]
        return None

    async def token_update(self, character_id, token_access, token_refresh, updated):
        self.sqlquery = """
                        REPLACE INTO `token_storage`
                        (`character_id`, `token_access`, `token_refresh`, `updated`)
                        VALUES ('{0}', '{1}', '{2}', '{3}')
                        """.format(character_id, token_access, token_refresh, updated)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def token_delete(self, character_id):
        self.sqlquery = "DELETE FROM `token_storage` WHERE `character_id`='{}'".format(character_id)
        await self.sql_query_exec(self.sqlquery)
        return None

        
class DBStart(DB):
    def sql_query(self, query):
        try:
            self.cursor.execute(query)
            self.sqlout = self.cursor.fetchall()
        except mysqldb.Error as e:
            if config.bot["devMode"]:
                print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            if config.bot["devMode"]:
                print("{}\n".format(query))
        return self.sqlout

    def sql_query_one(self, query):
        try:
            self.cursor.execute(query)
            self.sqlout = self.cursor.fetchone()
            return self.sqlout
        except mysqldb.Error as e:
            if config.bot["devMode"]:
                print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            if config.bot["devMode"]:
                print("{}\n".format(query))

    def sql_query_exec(self, query):
        try:
            self.cursor.execute(query)
            self.cnx.commit()
            return 0
        except mysqldb.Error as e:
            if config.bot["devMode"]:
                print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            if config.bot["devMode"]:
                print("{}\n".format(query))

    def mysql_version(self):
        self.sqlquery = "SELECT version()"
        self.sqlout = self.sql_query(self.sqlquery)
        if self.sqlout is not None:
            return self.sqlout[0]['version()']
        return None

    def db_version(self):
        self.sqlquery = "SELECT version()"
        self.sqlout = self.sql_query(self.sqlquery)
        if self.sqlout is not None:
            return self.sqlout[0]['version()']
        return None

    def storage_add(self, key, value):
        self.sqlquery = "REPLACE INTO `storage` (`s_key`, `s_value`) VALUES ('{0}', '{1}')".format(key, value)
        self.sql_query_exec(self.sqlquery)
        return None

    def storage_get(self, key):
        self.sqlquery = "SELECT s_value FROM `storage` WHERE `s_key`='{}'".format(key)
        self.sqlout = self.sql_query_one(self.sqlquery)
        if self.sqlout is not None:
            return self.sqlout
        return None

    def message_check(self):
        self.sqlquery = "SELECT * FROM `queue_message`"
        self.sqlout = self.sql_query(self.sqlquery)
        if len(self.sqlout) > 35:
            self.clearMessageQueue()
        return None

    def message_clear(self):
        self.sqlquery = "DELETE from `queue_message`"
        self.sql_query_exec(self.sqlquery)
        if config.bot["devMode"]:
            print("Cache was cleaned")
        else:
            log.info("Cache was cleaned")
        return None
