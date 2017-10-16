#============================================================================
#	functions for working with DB
#============================================================================

import asyncio
import mysql.connector as mysqldb
from mysql.connector import errorcode

from config import config
dbcfg = config.db

class db:
    async def connect(self):
        self.cnx = mysqldb.connect(** dbcfg)

    async def isconnected(self):
        try:
            if self.cnx.is_connected():
                return('Connected to MySQL database')
        except Error as e:
            return(e)
        finally:
            cnx.close()