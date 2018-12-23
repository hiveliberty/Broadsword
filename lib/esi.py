import asyncio
import aiohttp
import logging
import json
import base64

from __init__ import __version__
from config import config

log = logging.getLogger("library.esi")


class ESIApi:
    def __init__(self, auth=False):
        self.headers = {}
        self.endpoint_url = "https://esi.evetech.net"
        self.headers["X-User-Agent"] = "evecitadel-esi v.{}".format(__version__)
        self.headers["Accept"] = "application/json"
        #self.headers["If-None-Match"] = ""
        self.language = "en-us"
        self.datasource = "tranquility"

    #def __del__(self):
    #    for attr in ("headers", "endpoint_url",
    #                 "language", "datasource"):
    #        self.__dict__.pop(attr,None)
    #    del self

    async def _request(self, url):
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.text()
                        data = json.loads(data)
                        #if config.bot["devMode"]:
                        #    log.info("URL: {}".format(url))
                        #    log.info("Response Data: {}".format(self.data))
                        return data
                    else:
                        return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def _search(self, categories, strict, str):
        try:
            str = str.replace(" ", "%20")
            #url = ("{0}/v2/search/?categories={1}&datasource={2}"
            #       "&language={3}&search={4}&strict={5}").format(
            #            self.endpoint_url, categories, self.datasource,
            #            self.language, str, strict)
            url = ("{0}/v2/search/?categories={1}&datasource={2}"
                   "&language={3}&search={4}&strict={5}")
            url = url.format(
                self.endpoint_url, categories, self.datasource,
                self.language, str, strict)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def _selfclean(self, vars):
        for attr in vars: self.__dict__.pop(attr,None)

    async def char_get_id(self, name):
        try:
            result = await self._search("character", "false", name)
            #return char_id["character"]
            return result["character"]
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

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
            url = "{url}/v4/characters/{id}/?datasource={src}"
            url = url.format(url=self.endpoint_url, id=id, src=self.datasource)
            response = await self._request(url)
            return self.response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def char_get_name(self, id):
        # return Name
        try:
            data = await self.char_get_details(id)
            if data is not None:
                return data["name"]
            else:
                return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(("corp_data"))

    async def alliance_get_contacts(self, id, token):
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
            url = ("{0}/v1/alliances/{1}/contacts/?datasource={2}&token={3}")
            url = url.format(self.endpoint_url, id, self.datasource, token)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def alliance_get_corporations(self, id):
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
            url = "{url}/v1/alliances/{id}/corporations/?datasource={src}".\
                format(url=self.endpoint_url, id=id, src=self.datasource)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def alliance_get_details(self, id):
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
            url = "{url}/v3/alliances/{id}/?datasource={src}".\
                format(url=self.endpoint_url, id=id, src=self.datasource)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def alliance_get_name(self, id):
        # return Name
        try:
            data = await self.alliance_get_details(id)
            if data is not None:
                return data["name"]
            else:
                return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

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
            url = "{url}/v4/corporations/{id}/?datasource={src}".\
                format(url=self.endpoint_url, id=id, src=self.datasource)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def corp_get_name(self, id):
        # return Name
        try:
            data = await self.corp_get_details(id)
            if data is not None:
                return data["name"]
            else:
                return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def mails_get_headers(self, char_id, labels, token):
        # response content:
        #   'mail_id'
        #   'subject'
        #   'from'
        #   'timestamp'
        #   'labels': []
        #   'recipients': [{'recipient_type', 'recipient_id'},]
        try:
            url = ("{0}/v1/characters/{1}/mail/?datasource={2}"
                   "&labels={3}&token={4}")
            url = url.format(self.endpoint_url, char_id, self.datasource, labels, token)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def mails_get_mail(self, char_id, mail_id, token):
        # response content:
        #   'subject'
        #   'from'
        #   'timestamp'
        #   'recipients': [{'recipient_type', 'recipient_id'},]
        #   'body'
        #   'labels': []
        #   'read'
        try:
            url = "{0}/v1/characters/{1}/mail/{2}/?datasource={3}&token={4}"
            url = url.format(
                self.endpoint_url, char_id, mail_id, self.datasource, token)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def moon_get_details(self, id):
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
            url = "{url}/v1/universe/moons/{id}/?datasource={src}&language={lang}".\
                format(url=self.endpoint_url, id=id, src=self.datasource, lang=self.language)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def moon_get_name(self, id):
        # return Name
        try:
            data = await self.moon_get_details(id)
            if data is not None:
                return data["name"]
            else:
                return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def notifications_get(self, char_id, token):
        # response content:
        #   'notification_id'
        #   'sender_id'
        #   'sender_type'
        #   'text': []
        #   'timestamp'
        #   'type'
        try:
            url = ("{0}/v3/characters/{1}/notifications/?datasource={2}"
                   "&token={3}")
            url = url.format(self.endpoint_url, char_id, self.datasource, token)
            if config.bot["devMode"]:
                log.info("ESI Option Data: {}, {}, {}, {}"
                         .format(
                         self.endpoint_url, char_id, self.datasource, token))
                log.info("ESI Request Url: {}".format(url))
            response = await self._request(url)
            response = sorted(response, key=lambda k: k['notification_id'])
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def planet_get_details(self, id):
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
            url = "{url}/v1/universe/planets/{id}/?datasource={src}".\
                format(url=self.endpoint_url, id=id, src=self.datasource, lang=self.language)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def status_tq(self):
        # response content:
        #   'server_version'
        #   'players'
        #   'start_time'
        try:
            url = "{url}/v1/status/?datasource={src}".\
                format(url=self.endpoint_url, src=self.datasource)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def structure_get_details(self, id, token):
        # response content:
        #   'notification_id'
        #   'sender_id'
        #   'sender_type'
        #   'text': []
        #   'timestamp'
        #   'type'
        try:
            url = ("{0}/v2/universe/structures/{1}/?datasource={2}"
                   "&token={3}")
            url = url.format(self.endpoint_url, id, self.datasource, token)
            if config.bot["devMode"]:
                log.info("ESI Option Data: {}, {}, {}, {}"
                         .format(
                         self.endpoint_url, char_id, self.datasource, token))
                log.info("ESI Request Url: {}".format(url))
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

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
            url = "{url}/v4/universe/systems/{id}/?datasource={src}&language={lang}".\
                format(url=self.endpoint_url, id=id, src=self.datasource, lang=self.language)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def system_get_name(self, id):
        # return Name
        try:
            data = await self.system_get_details(id)
            if data is not None:
                return data["name"]
            else:
                return None
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def type_get_details(self, id):
        # return Name
        try:
            url = "{url}/v3/universe/types/{id}/?datasource={src}&language={lang}".\
                format(url=self.endpoint_url, id=id, src=self.datasource, lang=self.language)
            response = await self._request(url)
            return response
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
