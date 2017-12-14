#==============================================================================
#
#   Все связанное с API запросами
#
#==============================================================================

import asyncio
import aiohttp
import requests
import base64
import datetime
import json

from config import config
from lib.libdb import DBMain
from lib.utils import BasicUtils

#==============================================================================

class TokenError(Exception):
    pass


class TokenInvalidError(TokenError):
    pass


class TokenExpiredError(TokenError):
    pass


class NotRefreshableTokenError(TokenError):
    pass


class EVEToken:
    def __init__(self):
        self.url = "https://login.eveonline.com/oauth/token"
        self.grant_type = "refresh_token"
        self.datetime = datetime.datetime
        self.client_id = config.sso["clientID"]
        self.client_secret = config.sso["secretKey"]
        self.credentials = "{0}:{1}".format(self.client_id, self.client_secret)
        self.auth = base64.b64encode(self.credentials.encode('utf-8'))
        self.auth_string = 'Basic ' + self.auth.decode(encoding='utf-8')
        self.user_agent = 'BroadswordBot/{}'.format(BasicUtils.bot_version())

    def __del__(self):
        for attr in ("url", "grant_type", "datetime", "client_id",
                     "client_secret", "credentials", "auth", "auth_string",
                     "user_agent"):
            self.__dict__.pop(attr,None)
        del self

    async def expired(self):
        try:
            if await self.can_refresh():
                self.stored_token = await self.get_stored()
                if self.stored_token is None:
                    return
                self.time_expired = self.stored_token["updatedOn"] +\
                                    datetime.timedelta(seconds=config.sso["token_expiry"])
                self.time_now = self.datetime.now().replace(microsecond=0)
                if self.time_expired > self.time_now:
                    return False
                else:
                    return True
            else:
                raise TokenExpiredError()
        except Exception as e:
            print(e)
        finally:
            for attr in ("stored_token", "time_expired", "time_now"):
                self.__dict__.pop(attr,None)

    async def can_refresh(self):
        try:
            self.stored_token = await self.get_stored()
            if self.stored_token is None:
                return False
            if self.stored_token["refreshToken"]:
                return True
            else:
                return False
        except Exception as e:
            print(e)
        finally:
            for attr in ("stored_token"):
                self.__dict__.pop(attr,None)

    async def refresh(self):
        try:
            self.stored_token = await self.get_stored()
            self.custom_headers = {
                'User-Agent': self.user_agent,
                'Content-Type': 'application/json',
                'Authorization': self.auth_string,
            }
            self.params = {
                'grant_type': self.grant_type,
                'refresh_token': self.stored_token["refreshToken"],
            }
            self.request = await aiohttp.post(self.url,
                                              params=self.params,
                                              headers=self.custom_headers)
            if self.request.status in [400, 403]:
                raise TokenInvalidError()
            self.response = await self.request.json()
            self.created = self.datetime.now().replace(microsecond=0)
            self.access_token = self.response["access_token"]
            self.refresh_token = self.response["refresh_token"]
            #print("New access token: {}".format(self.access_token))
            #print("Old access token: {}".format(self.stored_token["accessToken"]))
            self.cnx = DBMain()
            await self.cnx.update_token_data(config.sso["character_id"],
                                             self.access_token,
                                             self.refresh_token,
                                             self.created)
        except Exception as e:
            print(e)
        finally:
            for attr in ("cnx", "stored_token", "custom_headers",
                         "params", "request", "response",
                         "access_token", "refresh_token"):
                self.__dict__.pop(attr,None)
        
    async def get_stored(self):
        try:
            self.cnx = DBMain()
            self.query = await self.cnx.get_token_data(config.sso["character_id"])
            return self.query
        except Exception as e:
            print(e)
        finally:
            for attr in ("cnx", "query"):
                self.__dict__.pop(attr,None)

    async def token(self):
        try:
            if await self.expired():
                if await self.can_refresh():
                    await self.refresh()
                else:
                    raise NotRefreshableTokenError()
            self.token = await self.get_stored()
            return self.token["accessToken"]
        except Exception as e:
            print(e)
        finally:
            for attr in ("token", "can_refresh", "expired"):
                self.__dict__.pop(attr,None)
