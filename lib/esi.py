#=============================================================================#
#                                                                             #
#                   empty lib for future implementation                       #
#                                                                             #
#=============================================================================#
import asyncio
import aiohttp
import logging
import json
import base64

from config import config
from lib.token import EVEToken
from lib.utils import BasicUtils

log = logging.getLogger("library.esi")
#log = logging.getLogger(__name__)

class ESIApi:
    def __init__(self, auth=False):
        self.headers = {}
        self.endpoint_url = "https://esi.tech.ccp.is"
        self.headers["User-Agent"] = "BroadswordBot v.{}".format(BasicUtils.bot_version())
        self.headers["Accept"] = "application/json"
        self.language = "en-us"
        self.datasource = "tranquility"

    def __del__(self):
        for attr in ("headers", "endpoint_url",
                     "language", "datasource"):
            self.__dict__.pop(attr,None)
        del self

    async def status_tq(self, id):
        # response content:
        #   'server_version'
        #   'players'
        #   'start_time'
        try:
            self.url = "{url}/v1/status/?datasource={src}".\
                format(url=self.endpoint_url, src=self.datasource)
            async with aiohttp.ClientSession(headers=self.headers) as self.session:
                async with self.session.get(self.url) as self.resp:
                    if self.resp.status == 200:
                        self.data = await self.resp.text()
                        self.data = json.loads(self.data)
                        return self.data
                    else:
                        return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("url", "resp", "data"):
                self.__dict__.pop(attr,None)

    async def char_get_details(self, id):
        # response content:
        #   'race_id'
        #   'gender'
        #   'alliance_id'
        #   'description'
        #   'security_status'
        #   'birthday'
        #   'bloodline_id'
        #   'ancestry_id'
        #   'corporation_id'
        #   'name'
        try:
            self.url = "{url}/v4/characters/{id}/?datasource={src}".\
                format(url=self.endpoint_url, id=id, src=self.datasource)
            async with aiohttp.ClientSession(headers=self.headers) as self.session:
                async with self.session.get(self.url) as self.resp:
                    if self.resp.status == 200:
                        self.data = await self.resp.text()
                        self.data = json.loads(self.data)
                        return self.data
                    else:
                        return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("url", "resp", "data"):
                self.__dict__.pop(attr,None)

    async def corp_get_details(self, id):
        # response content:
        #   'url'
        #   'tax_rate'
        #   'shares'
        #   'ceo_id'
        #   'home_station_id'
        #   'name'
        #   'member_count'
        #   'description'
        #   'alliance_id'
        #   'creator_id'
        #   'date_founded'
        #   'ticker'
        try:
            self.url = "{url}/v4/corporations/{id}/?datasource={src}".\
                format(url=self.endpoint_url, id=id, src=self.datasource)
            async with aiohttp.ClientSession(headers=self.headers) as self.session:
                async with self.session.get(self.url) as self.resp:
                    if self.resp.status == 200:
                        self.data = await self.resp.text()
                        self.data = json.loads(self.data)
                        return self.data
                    else:
                        return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("url", "resp", "data"):
                self.__dict__.pop(attr,None)

    async def corp_get_name(self, id):
        # return Name
        try:
            self.corp_data = await self.corp_get_details(id)
            if self.corp_data is not None:
                return self.corp_data["name"]
            else:
                return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("system_data"):
                self.__dict__.pop(attr,None)

    async def system_get_details(self, id):
        # response content:
        #   'star_id'
        #   'system_id'
        #   'name'
        #   'position'
        #   'security_status'
        #   'constellation_id'
        #   'planets': [{"planet_id":40000041,"moons":[40000042]},...]
        #   'security_class'
        #   'stargates': [0,0,...]
        try:
            self.url = "{url}/v3/universe/systems/{id}/?datasource={src}&language={lang}".\
                format(url=self.endpoint_url, id=id, src=self.datasource, lang=self.language)
            async with aiohttp.ClientSession(headers=self.headers) as self.session:
                async with self.session.get(self.url) as self.resp:
                    if self.resp.status == 200:
                        self.data = await self.resp.text()
                        self.data = json.loads(self.data)
                        return self.data
                    else:
                        return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("url", "resp", "data"):
                self.__dict__.pop(attr,None)

    async def system_get_name(self, id):
        # return Name
        try:
            self.system_data = await self.system_get_details(id)
            if self.system_data is not None:
                return self.system_data["name"]
            else:
                return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("system_data"):
                self.__dict__.pop(attr,None)

    async def type_get_name(self, id):
        # return Name
        try:
            self.url = "{url}/v3/universe/types/{id}/?datasource={src}&language={lang}".\
                format(url=self.endpoint_url, id=id, src=self.datasource, lang=self.language)
            async with aiohttp.ClientSession(headers=self.headers) as self.session:
                async with self.session.get(self.url) as self.resp:
                    if self.resp.status == 200:
                        self.data = await self.resp.text()
                        self.data = json.loads(self.data)
                        return self.data["name"]
                    else:
                        return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("url", "resp", "data"):
                self.__dict__.pop(attr,None)
