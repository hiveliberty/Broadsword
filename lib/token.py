#==============================================================================
#
#   Library for work with token
#
#==============================================================================

import logging
import asyncio
import aiohttp
import requests
import base64
import datetime
import json

from config import config
from lib.db import DBMain
from lib.utils import BasicUtils

#==============================================================================

log = logging.getLogger("library.token")

class TokenError(Exception):
    pass


class TokenInvalidError(TokenError):
    pass


class TokenExpiredError(TokenError):
    pass


class NotRefreshableTokenError(TokenError):
    pass


class EVEToken:
    def __init__(self, char_id):
        self.url = "https://login.eveonline.com/oauth/token"
        self.grant_type = "refresh_token"
        self.datetime = datetime.datetime
        self.char_id = char_id
        self.client_id = config.sso["clientID"]
        self.client_secret = config.sso["secretKey"]
        self.credentials = "{0}:{1}".format(self.client_id, self.client_secret)
        self.auth = base64.b64encode(self.credentials.encode('utf-8'))
        self.auth_string = 'Basic ' + self.auth.decode(encoding='utf-8')
        self.user_agent = 'BroadswordBot/{}'.format(BasicUtils.bot_version())

    def __del__(self):
        for attr in ("url", "grant_type", "datetime", "client_id",
                     "client_secret", "credentials", "auth", "auth_string",
                     "user_agent", "char_id"):
            self.__dict__.pop(attr,None)
        del self

    async def _selfclean(self, vars):
        for attr in vars: self.__dict__.pop(attr,None)

    async def _can_refresh(self):
        try:
            if self.stored_token is None:
                return False
            if self.stored_token["token_refresh"]:
                return True
            else:
                return False
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def _expired(self):
        try:
            if await self._can_refresh():
                self.time_expired = self.stored_token["updated"] +\
                                    datetime.timedelta(seconds=config.sso["token_expiry"])
                self.time_now = self.datetime.now().replace(microsecond=0)
                if self.time_expired > self.time_now:
                    return False
                else:
                    return True
            else:
                raise NotRefreshableTokenError()
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def _get_stored(self):
        try:
            self.cnx = DBMain()
            self.stored_token = await self.cnx.token_get(self.char_id)
            if config.bot["devMode"]:
                log.info("Stored token: {}".format(self.stored_token))
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(("cnx"))

    async def _refresh(self):
        try:
            self.custom_headers = {
                "User-Agent": self.user_agent,
                "Content-Type": "application/json",
                "Authorization": self.auth_string,
            }
            self.params = {
                "grant_type": self.grant_type,
                "refresh_token": self.stored_token["token_refresh"],
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
            self.cnx = DBMain()
            await self.cnx.token_update(config.sso["character_id"],
                                             self.access_token,
                                             self.refresh_token,
                                             self.created)
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            if config.bot["devMode"]:
                log.info("Old token: {}".format(self.stored_token["token_access"]))
                log.info("New token: {}".format(self.access_token))
            await self._selfclean(("cnx"))

    async def get_token(self):
        try:
            await self._get_stored()
            if await self._expired():
                await self._refresh()
            else:
                self.access_token = self.stored_token["token_access"]
            return self.access_token
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(
                ("stored_token", "time_expired", "time_now", "custom_headers",
                 "params", "request", "response", "created", "access_token",
                 "refresh_token")
            )
