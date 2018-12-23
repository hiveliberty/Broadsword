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
import json
from datetime import datetime, timedelta

from __init__ import __version__
from config import config
from lib.db import DBMain
# from lib.utils import BasicUtils

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
    def __init__(self):
        self.url = "https://login.eveonline.com/oauth/token"
        self.grant_type = "refresh_token"
        # self.datetime = datetime.datetime
        # self.char_id = char_id
        self.client_id = config.sso["clientID"]
        self.client_secret = config.sso["secretKey"]
        self.credentials = "{0}:{1}".format(self.client_id, self.client_secret)
        self.auth = base64.b64encode(self.credentials.encode('utf-8'))
        self.auth_string = 'Basic ' + self.auth.decode(encoding='utf-8')
        self.user_agent = 'BroadswordBot/{}'.format(__version__)
        self.token = {}

    # def __del__(self):
        # for attr in ("url", "grant_type", "datetime", "client_id",
                     # "client_secret", "credentials", "auth", "auth_string",
                     # "user_agent", "char_id"):
            # self.__dict__.pop(attr,None)
        # del self

    async def _selfclean(self, vars):
        for attr in vars: self.__dict__.pop(attr,None)

    async def _can_refresh(self):
        try:
            if self.stored_token is None:
                return False
            if self.stored_token["refresh_token"]:
                return True
            else:
                return False
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def _expired(self):
        try:
            if await self._can_refresh():
                # self.time_expired = self.stored_token["updated"] +\
                                    # datetime.timedelta(seconds=config.sso["token_expiry"])
                # self.time_now = self.datetime.now().replace(microsecond=0)
                # if self.time_expired > self.time_now:
                    # return False
                # else:
                    # return True
                time_expired = self.stored_token["expire_date"]
                time_now = datetime.now().replace(microsecond=0)
                if time_expired > time_now:
                    return False
                else:
                    return True
            else:
                raise NotRefreshableTokenError()
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def _get_stored(self, type, scope):
        try:
            cnx = DBMain()
            self.stored_token = await cnx.token_get(type, scope)
            del cnx
            if config.bot["devMode"]:
                log.info("Stored token: {}".format(self.stored_token))
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def _refresh(self):
        try:
            custom_headers = {
                "User-Agent": self.user_agent,
                "Content-Type": "application/json",
                "Authorization": self.auth_string,
            }
            params = {
                "grant_type": self.grant_type,
                "refresh_token": self.stored_token["refresh_token"],
            }
            request = await aiohttp.post(self.url,
                                              params=params,
                                              headers=custom_headers)
            if request.status in [400, 403]:
                raise TokenInvalidError()
            response = await request.json()
            log.info(
                "Datetime now: {}"
                .format(datetime.now().replace(microsecond=0)))
            expire_date = (
                datetime.now().replace(microsecond=0)
                + timedelta(seconds=config.notifications["token_expiry"]))
            access_token = response["access_token"]
            refresh_token = response["refresh_token"]
            cnx = DBMain()
            await cnx.token_update(
                self.stored_token["character_id"],
                access_token,
                self.stored_token["scope_name"],
                expire_date)
            self.token["access_token"] = access_token
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            if config.bot["devMode"]:
                log.info("Old token: {}".format(self.stored_token["access_token"]))
                log.info("New token: {}".format(access_token))

    async def get_token(self, type, scope):
        try:
            await self._get_stored(type, scope)
            if await self._expired():
                await self._refresh()
            else:
                self.token["access_token"] = self.stored_token["access_token"]
            self.token["character_id"] = self.stored_token["character_id"]
            return self.token
        except Exception as e:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(
                ("stored_token", "time_expired", "time_now", "custom_headers",
                 "params", "request", "response", "created", "access_token",
                 "refresh_token")
            )
