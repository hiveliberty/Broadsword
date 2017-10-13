#============================================================================
#	functions for working with DB
#============================================================================

import asyncio
import mysql.connector as mysqldb
from mysql.connector import errorcode

class db:
    async def __init__(self, cfg):
        self.cnx = mysqldb.connect(** cfg)
        return None

    async def test(self):
        try:
            if self.cnx.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(e)
        finally:
            cnx.close()