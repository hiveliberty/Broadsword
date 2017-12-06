#============================================================================
#	functions for working with DB
#   
#   Class DB is actual for use
#   Class DBStart is actual for use
#============================================================================

import asyncio
import mysql.connector as mysqldb
#from mysql.connector import errorcode
from config.config import db as dbcfg


class DB:
    def __init__(self):
        try:
            self.cnx = mysqldb.connect(**dbcfg)
            self.cursor = self.cnx.cursor(dictionary=True)
            print('Database connection opened')
        except mysqldb.Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))

    def __del__(self):
        try:
            self.cursor.close()
            print('Cursor closed')
            self.cnx.close()
            print('Database connection closed')
        except mysqldb.Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))

    async def sqlQuery(self, query):
        try:
            self.cursor.execute(query)
            self.sqlout = self.cursor.fetchall()
            return self.sqlout
        except mysqldb.Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            print("{}\n".format(query))
        #return self.sqlout

    async def sqlQueryExec(self, query):
        try:
            self.cursor.execute(query)
            self.cnx.commit()
            return 0
        except mysqldb.Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            print("{}\n".format(query))

    async def addDiscordUser(self, discordID):
        self.sqlquery = "INSERT INTO `discordUsers` SET discordID='{0}'".format(discordID)
        #self.sqlquery = "REPLACE INTO `discordUsers` (discordID, isAuthorized) VALUES ('{0}', 'no')".format(discordID)
        await self.sqlQueryExec(self.sqlquery)
        return None

    async def setAuthorized(self, discordID):
        self.sqlquery = "UPDATE `discordUsers` SET isAuthorized='yes' WHERE discordID='{}'".format(discordID)
        await self.sqlQueryExec(self.sqlquery)
        return None

    async def setUnauthorized(self, discordID):
        self.sqlquery = "UPDATE `discordUsers` SET isAuthorized='no' WHERE discordID='{}'".format(discordID)
        await self.sqlQueryExec(self.sqlquery)
        return None
        
    async def delDiscordUser(self, discordID):
        self.sqlquery = "DELETE FROM `discordUsers` WHERE discordID='{}'".format(discordID)
        await self.sqlQueryExec(self.sqlquery)
        return None

    async def insertTestUser(self, characterID, corporationID, allianceID, authString, active):
        self.sqlquery = "REPLACE INTO `pendingUsers` (characterID, corporationID, allianceID, authString, active) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(characterID, corporationID, allianceID, authString, active)
        await self.sqlQueryExec(self.sqlquery)
        return None
        
    async def insertUser(self, characterID, discordID, eveName):
        self.sqlquery = "REPLACE INTO `authUsers` (characterID, discordID, eveName, active) VALUES ('{0}','{1}','{2}','yes')".format(characterID, discordID, eveName)
        await self.sqlQueryExec(self.sqlquery)
        return None
    
    async def disableReg(self, authCode):
        self.sqlquery = "UPDATE `pendingUsers` SET active='0' WHERE authString='{}'".format(authCode)
        await self.sqlQueryExec(self.sqlquery)
        return None
        
    async def disableUser(self, characterID):
        self.sqlquery = "UPDATE `authUsers` SET active='no' WHERE characterID='{}'".format(characterID)
        await self.sqlQueryExec(self.sqlquery)
        return None
    
    async def selectPending(self, authCode):
        self.sqlquery = "SELECT * FROM `pendingUsers` WHERE authString='{}' AND active='1'".format(authCode)
        self.sqlout = await self.sqlQuery(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]
        print(self.sqlout)
        return None

    async def selectUsers(self):
        self.sqlquery = "SELECT discordID, characterID, eveName FROM `authUsers` where active='yes'"
        self.sqlout = await self.sqlQuery(self.sqlquery)
        print(self.sqlout)
        return self.sqlout

    async def addQueueMessage(self, msg, channel):
        self.sqlquery = "INSERT INTO `messageQueue` (message, channel) VALUES ('{0}', '{1}')".format(msg, channel)
        await self.sqlQueryExec(self.sqlquery)
        return None

    async def getQueuedMessage(self, id):
        self.sqlquery = "SELECT * FROM `messageQueue` WHERE id='{}'".format(id)
        self.sqlout = await self.sqlQuery(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]
        return None

    async def gelOldestQueueMessage(self):
        self.sqlquery = "SELECT MIN(id) FROM `messageQueue`"
        self.sqlout = await self.sqlQuery(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]['MIN(id)']
        return None

    async def delQueuedMessage(self, id):
        self.sqlquery = "DELETE FROM `messageQueue` WHERE id='{}'".format(id)
        await self.sqlQueryExec(self.sqlquery)
        return None

    async def setMaxPrioQueueMessage(self, msg, channel):
        self.oldest = await self.gelOldestQueueMessage()
        if self.oldest is not None:
            self.sqlquery = "INSERT INTO `messageQueue` (id, message, channel) VALUES ('{0}', '{1}', '{2}')".format(self.id, msg, channel)
            await self.sqlQueryExec(self.sqlquery)
        return None

    async def addQueueRename(self, discordID, nick):
        self.sqlquery = "INSERT INTO `renameQueue` (discordID, nick) VALUES ('{0}', '{1}')".format(discordID, nick)
        await self.sqlQueryExec(self.sqlquery)
        return None

    async def getQueuedRename(self, id):
        self.sqlquery = "SELECT * FROM `renameQueue` WHERE id='{}'".format(id)
        self.sqlout = await self.sqlQuery(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]
        return None

    async def gelOldestQueueRename(self):
        self.sqlquery = "SELECT MIN(id) FROM `renameQueue`"
        self.sqlout = await self.sqlQuery(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]['MIN(id)']
        return None

    async def delQueuedRename(self, id):
        self.sqlquery = "DELETE FROM `renameQueue` WHERE id='{}'".format(id)
        await self.sqlQueryExec(self.sqlquery)
        return None

    async def addCorpInfo(self, corpID, corpTicker, corpName, corpRole):
        self.sqlquery = "REPLACE INTO `corpCache` (corpID, corpTicker, corpName, corpRole) VALUES ('{0}', '{1}', '{2}', '{3}')".format(corpID, corpTicker, corpName, corpRole)
        await self.sqlQueryExec(self.sqlquery)
        return None

    async def getCorpInfo(self, corpID):
        self.sqlquery = "SELECT * FROM `corpCache` WHERE corpID='{}'".format(corpID)
        self.sqlout = await self.sqlQuery(self.sqlquery)
        if len(self.sqlout) == 0:
            return
        return self.sqlout[0]

    async def delCorpInfo(self, corpID):
        self.sqlquery = "DELETE FROM `corpCache` WHERE corpID='{}'".format(corpID)
        await self.sqlQueryExec(self.sqlquery)
        return None

    async def setKey(self, key, value):
        self.sqlquery = "REPLACE INTO `storage` (`storedKey`, `storedValue`) VALUES ('{0}', '{1}')".format(key, value)
        await self.sqlQueryExec(self.sqlquery)
        return None

    async def getKey(self, key):
        self.sqlquery = "SELECT value FROM `storage` WHERE `storedKey`='{}'".format(key)
        self.sqlout = await self.sqlQuery(self.sqlquery)
        if len(self.sqlout) >= 1:
            return self.sqlout[0]['value']
        return None

    async def delKey(self, key):
        self.sqlquery = "DELETE FROM `storage` WHERE `storedKey`='{}'".format(key)
        await self.sqlQueryExec(self.sqlquery)
        return None
        
class DBStart:
    def __init__(self):
        try:
            self.cnx = mysqldb.connect(**dbcfg)
            self.cursor = self.cnx.cursor(dictionary=True)
            print('Database connection opened')
        except mysqldb.Error as e:
            #print('ERROR %s' % (e.args[1]))
            print("Error code: {}".format(e.errno))
            print("Error message: {}".format(e.msg))
            return None

    def __del__(self):
        try:
            self.cursor.close()
            print('Cursor closed')
            self.cnx.close()
            print('Database connection closed')
        except mysqldb.Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))

    def sql_query(self, query):
        try:
            self.cursor.execute(query)
            self.sqlout = self.cursor.fetchall()
        except mysqldb.Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            print("{}\n".format(query))
        return self.sqlout

    def sql_query_one(self, query):
        try:
            self.cursor.execute(query)
            self.sqlout = self.cursor.fetchone()
        except mysqldb.Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
            print("{}\n".format(query))
        return self.sqlout

    def sql_query_exec(self, query):
        try:
            self.cursor.execute(query)
            self.cnx.commit()
            return 0
        except mysqldb.Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        finally:
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

    def set_key(self, key, value):
        self.sqlquery = "REPLACE INTO `storage` (`storedKey`, `storedValue`) VALUES ('{0}', '{1}')".format(key, value)
        self.sql_query_exec(self.sqlquery)
        return None

    def get_key(self, key):
        self.sqlquery = "SELECT storedValue FROM `storage` WHERE `storedKey`='{}'".format(key)
        self.sqlout = self.sql_query_one(self.sqlquery)
        if self.sqlout is not None:
            return self.sqlout
        return None

    def check_message_queue(self):
        self.sqlquery = "SELECT * FROM messageQueue"
        self.sqlout = self.sql_query(self.sqlquery)
        if len(self.sqlout) > 35:
            self.clearMessageQueue()
        print("Cache was checked")
        return None

    def clear_message_queue(self):
        self.sqlquery = "DELETE from messageQueue"
        self.sql_query_exec(self.sqlquery)
        print("Cache was cleaned")
        return None


class DBBot:
    def __init__(self):
        try:
            self.cnx = mysqldb.connect(**dbcfg)
            self.cursor = self.cnx.cursor()
            print('Database connection opened')
        except Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))

    def __del__(self):
        self.cursor.close()
        self.cnx.close()
        print('Database connection closed')

    def setKey(self, key, value):
        self.sqlquery = "REPLACE INTO storage (`key`, `value`) VALUES ('{0}', '{1}')".format(key, value)
        self.cursor.execute(self.sqlquery)

    def getKey(self, key):
        self.sqlquery = "SELECT value FROM storage WHERE `key` = :key COLLATE NOCASE".format(authCode)
        try:
            self.cursor.execute(self.sqlquery)
            self.sqlout = self.cursor.fetchall()
        except Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        print("{}\n".format(self.sqlquery))
        return self.sqlout