#============================================================================
#	functions for working with DB
#   
#   Class DBAuth is actual for use
#============================================================================

import asyncio
import mysql.connector as mysqldb
from mysql.connector import errorcode
from config.config import db as dbcfg

class DB:
    def __init__(self, cfg):
        self.db_conf = cfg
        try:
            self.cnx = mysqldb.connect(**self.db_conf)
            self.cursor = self.cnx.cursor()
            print('Database connection opened')
        except Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
    
    def request(self, sql):
        self.cursor.execute(sql)
        self.sqlout = self.cursor.fetchall()
        return self.sqlout
        
    def insertTestUser(self, characterID, corporationID, allianceID, groups, authString, active):
        self.sqlquery = "INSERT INTO `pendingUsers` (characterID, corporationID, allianceID, groups, authString, active) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(characterID, corporationID, allianceID, groups, authString, active)
        try:
            self.cursor.execute(self.sqlquery)
            self.cnx.commit()
        except Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        print("{}\n".format(self.sqlquery))
        
    def insertUser(self, userID, characterID, eveName, type):
        self.sqlquery = "REPLACE INTO `authUsers` (characterID, discordID, eveName, active, role) VALUES ('{0}','{1}','{2}','yes','{3}')".format(userID, characterID, eveName, type)
        self.cursor.execute(self.sqlquery)
    
    def disableReg(self, authCode):
        self.sqlquery = "UPDATE pendingUsers SET active='0' WHERE authString='{}'".format(authCode)
        self.cursor.execute(self.sqlquery)
    
    def selectPending(self, authCode):
        self.sqlquery = "SELECT * FROM pendingUsers WHERE authString='{}' AND active='1'".format(authCode)
        try:
            self.cursor.execute(self.sqlquery)
            self.sqlout = self.cursor.fetchall()
        except Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        print("{}\n".format(self.sqlquery))
        return self.sqlout
        
    def __del__(self):
        self.cursor.close()
        self.cnx.close()
        print('Database connection closed')

class DBTemp:
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

class DBAuth:
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
    
    def insertTestUser(self, characterID, corporationID, allianceID, groups, authString, active):
        self.sqlquery = "INSERT INTO `pendingUsers` (characterID, corporationID, allianceID, groups, authString, active) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(characterID, corporationID, allianceID, groups, authString, active)
        try:
            self.cursor.execute(self.sqlquery)
            self.cnx.commit()
        except Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        print("{}\n".format(self.sqlquery))
        
    def insertUser(self, userID, characterID, eveName, type):
        self.sqlquery = "REPLACE INTO `authUsers` (characterID, discordID, eveName, active, role) VALUES ('{0}','{1}','{2}','yes','{3}')".format(userID, characterID, eveName, type)
        try:
            self.cursor.execute(self.sqlquery)
            self.cnx.commit()
        except Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        print("{}\n".format(self.sqlquery))
    
    def disableReg(self, authCode):
        self.sqlquery = "UPDATE pendingUsers SET active='0' WHERE authString='{}'".format(authCode)
        try:
            self.cursor.execute(self.sqlquery)
            self.cnx.commit()
        except Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        print("{}\n".format(self.sqlquery))
    
    def selectPending(self, authCode):
        self.sqlquery = "SELECT * FROM pendingUsers WHERE authString='{}' AND active='1'".format(authCode)
        try:
            self.cursor.execute(self.sqlquery)
            self.sqlout = self.cursor.fetchall()
        except Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
        print("{}\n".format(self.sqlquery))
        return self.sqlout


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