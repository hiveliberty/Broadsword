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

log = logging.getLogger("library")

class DB:
    def __init__(self):
        try:
            self.cnx = mysqldb.connect(**dbcfg)
            self.cursor = self.cnx.cursor(dictionary=True)
            if config.bot["devMode"]:
                print('Database connection opened')
        except mysqldb.Error as e:
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
            if config.bot["devMode"]:
                print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            if config.bot["devMode"]:
                print("{}\n".format(query))

    async def discord_add_user(self, discordID):
        self.sqlquery = "REPLACE INTO `discordUsers` SET discordID='{0}'".format(discordID)
        #self.sqlquery = "INSERT INTO `discordUsers` SET discordID='{0}'".format(discordID)
        #self.sqlquery = "REPLACE INTO `discordUsers` (discordID, isAuthorized) VALUES ('{0}', 'no')".format(discordID)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def discord_set_authorized(self, discordID):
        self.sqlquery = "UPDATE `discordUsers` SET isAuthorized='yes' WHERE discordID='{}'".format(discordID)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def discord_set_unauthorized(self, discordID):
        self.sqlquery = "UPDATE `discordUsers` SET isAuthorized='no' WHERE discordID='{}'".format(discordID)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def discord_delete_user(self, discordID):
        self.sqlquery = "DELETE FROM `discordUsers` WHERE discordID='{}'".format(discordID)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def insert_user(self, characterID, discordID, eveName):
        self.sqlquery = """
                        REPLACE INTO `authUsers`
                        (characterID, discordID, eveName, active)
                        VALUES ('{0}','{1}','{2}','yes')
                        """.format(characterID, discordID, eveName)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def auth_enabled(self, characterID):
        self.sqlquery = "UPDATE `authUsers` SET pending='yes' WHERE characterID='{}'".format(characterID)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def auth_disable(self, characterID):
        self.sqlquery = "UPDATE `authUsers` SET pending='no' WHERE characterID='{}'".format(characterID)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def user_enabled(self, characterID):
        self.sqlquery = "UPDATE `authUsers` SET active='yes' WHERE characterID='{}'".format(characterID)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def user_update(self, characterID, key, value):
        self.sqlquery = "UPDATE `authUsers` SET {1}='{2}' WHERE characterID='{0}'".format(characterID, key, value)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def user_disable(self, characterID):
        self.sqlquery = "UPDATE `authUsers` SET active='no' WHERE characterID='{}'".format(characterID)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def select_pending(self):
        self.sqlquery = """SELECT *
                           FROM `authUsers`
                           WHERE pending='yes'"""
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]
        return None

    async def select_users(self):
        self.sqlquery = """SELECT discordID, characterID, eveName
                           FROM `authUsers`
                           WHERE active='yes' AND pending='no'"""
        self.sqlout = await self.sql_query(self.sqlquery)
        return self.sqlout

    async def message_add(self, msg, channel):
        self.sqlquery = "INSERT INTO `messageQueue` (message, channel) VALUES ('{0}', '{1}')".format(msg, channel)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def message_get(self, id):
        self.sqlquery = "SELECT * FROM `messageQueue` WHERE id='{}'".format(id)
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]
        return None

    async def message_get_oldest(self):
        self.sqlquery = "SELECT MIN(id) FROM `messageQueue`"
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]['MIN(id)']
        return None

    async def message_delete(self, id):
        self.sqlquery = "DELETE FROM `messageQueue` WHERE id='{}'".format(id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def message_set_maxprio(self, msg, channel):
        self.oldest = await self.message_get_oldest()
        if self.oldest is not None:
            self.sqlquery = """
                            INSERT INTO `messageQueue`
                            (id, message, channel)
                            VALUES ('{0}', '{1}', '{2}')
                            """.format(self.id, msg, channel)
            await self.sql_query_exec(self.sqlquery)
        return None

    async def rename_add(self, discordID, nick):
        self.sqlquery = "INSERT INTO `renameQueue` (discordID, nick) VALUES ('{0}', '{1}')".format(discordID, nick)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def rename_get(self, id):
        self.sqlquery = "SELECT * FROM `renameQueue` WHERE id='{}'".format(id)
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]
        return None

    async def rename_get_oldest(self):
        self.sqlquery = "SELECT MIN(id) FROM `renameQueue`"
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]['MIN(id)']
        return None

    async def rename_delete(self, id):
        self.sqlquery = "DELETE FROM `renameQueue` WHERE id='{}'".format(id)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def corpinfo_add(self, corpID, corpTicker, corpName, corpRole):
        self.sqlquery = """
                        REPLACE INTO `corpCache`
                        (corpID, corpTicker, corpName, corpRole)
                        VALUES ('{0}', '{1}', '{2}', '{3}')
                        """.format(corpID, corpTicker, corpName, corpRole)
        await self.sql_query_exec(self.sqlquery)
        return None
        
    async def corpinfo_update(self, corpID, key, value):
        self.sqlquery = "UPDATE `corpCache` SET {1}='{2}' WHERE corpID='{0}'".format(corpID, key, value)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def corpinfo_get(self, corpID):
        self.sqlquery = "SELECT * FROM `corpCache` WHERE corpID='{}'".format(corpID)
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) == 0:
            return
        return self.sqlout[0]

    async def corpinfo_delete(self, corpID):
        self.sqlquery = "DELETE FROM `corpCache` WHERE corpID='{}'".format(corpID)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def storage_add(self, key, value):
        self.sqlquery = "REPLACE INTO `storage` (`storedKey`, `storedValue`) VALUES ('{0}', '{1}')".format(key, value)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def storage_update(self, key, value):
        self.sqlquery = "UPDATE `storage` SET storedValue='{1}' WHERE storedKey='{0}'".format(key, value)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def storage_get(self, key):
        self.sqlquery = "SELECT storedValue FROM `storage` WHERE `storedKey`='{}'".format(key)
        self.sqlout = await self.sql_query(self.sqlquery)
        print(self.sqlout)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]['storedValue']
        return None

    async def storage_delete(self, key):
        self.sqlquery = "DELETE FROM `storage` WHERE `storedKey`='{}'".format(key)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def token_get(self, characterID):
        self.sqlquery = "SELECT * FROM `tokenStorage` WHERE `characterID`='{}'".format(characterID)
        self.sqlout = await self.sql_query(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]
        return None

    async def token_update(self, characterID, accessToken, refreshToken, updatedOn):
        self.sqlquery = """
                        REPLACE INTO `tokenStorage`
                        (`characterID`, `accessToken`, `refreshToken`, `updatedOn`)
                        VALUES ('{0}', '{1}', '{2}', '{3}')
                        """.format(characterID, accessToken, refreshToken, updatedOn)
        await self.sql_query_exec(self.sqlquery)
        return None

    async def token_delete(self, characterID):
        self.sqlquery = "DELETE FROM `tokenStorage` WHERE `characterID`='{}'".format(characterID)
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
        self.sqlquery = "REPLACE INTO `storage` (`storedKey`, `storedValue`) VALUES ('{0}', '{1}')".format(key, value)
        self.sql_query_exec(self.sqlquery)
        return None

    def storage_get(self, key):
        self.sqlquery = "SELECT storedValue FROM `storage` WHERE `storedKey`='{}'".format(key)
        self.sqlout = self.sql_query_one(self.sqlquery)
        if self.sqlout is not None:
            return self.sqlout
        return None

    def message_check(self):
        self.sqlquery = "SELECT * FROM messageQueue"
        self.sqlout = self.sql_query(self.sqlquery)
        if len(self.sqlout) > 35:
            self.clearMessageQueue()
        return None

    def message_clear(self):
        self.sqlquery = "DELETE from messageQueue"
        self.sql_query_exec(self.sqlquery)
        if config.bot["devMode"]:
            print("Cache was cleaned")
        else:
            log.info("Cache was cleaned")
        return None
