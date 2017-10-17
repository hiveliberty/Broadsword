#============================================================================
#	functions for working with DB
#============================================================================

import asyncio
import mysql.connector as mysqldb
from mysql.connector import errorcode

class DB:
    def __init__(self, cfg):
        self.db_conf = cfg
        try:
            self.db_connect = mysqldb.connect(**self.db_conf)
            self.cursor = self.db_connect.cursor()
            print('Database connection opened')
        except Error as e:
            print('ERROR: %d: %s' % (e.args[0], e.args[1]))
    
    def request(self, sql):
        self.cursor.execute(sql)
        self.sqlout = self.cursor.fetchall()
        return self.sqlout
        
    def __del__(self):
        self.cursor.close()
        self.db_connect.close()
        print('Database connection closed')