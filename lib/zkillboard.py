#==============================================================================
#
#   Все связанное с API запросами
#
#==============================================================================

import asyncio
import aiohttp
import requests
import logging
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
#import xmltodict
import time
import json
#import lxml
#from lxml import etree

from lib.esi import ESIApi
from config import config
from lib.utils import BasicUtils

#==============================================================================
#version = await getVersion()

log = logging.getLogger("library.zkillboard")


class zKillboardAPI:
    #==============================================================================
    #   https://github.com/zKillboard/zKillboard/wiki/API-(Killmails)
    #==============================================================================
    def __init__(self, id):
        self.id = id
        self.user_agent = {'user-agent': 'BroadswordBot/{}'.format(BasicUtils.bot_version())}
        self.base_url = "https://zkillboard.com/api/"
        self.esi = ESIApi()
        self.request_url = self.base_url + "characterID/{}/limit/1/no-items/".format(self.id)
        try:
            self.response = requests.get(self.request_url)
            if self.response.status_code == 200:
                self.response = self.response.json()
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))

    # This reserved method, but is not good
    async def init(self):
        try:
            async with aiohttp.get(self.request_url) as self.response:
                print(self.response)
                if self.response.status == 200:
                    self.response = await self.response.json()
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def getLatestSystem(self):
        #async with aiohttp.get(self.request_url) as self.response:
        #    if self.response.status == 200:
        #        self.response = await self.response.json()
        try:
            self.temp = await self.esi.system_get_name(self.response[0]['solar_system_id'])
            return self.temp
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def getLastShipType(self):
        try:
            if self.response[0]['victim']['character_id'] == self.id:
                self.temp = await self.esi.type_get_name(self.response[0]['victim']['ship_type_id'])
                return self.temp
            else:
                for self.x in self.response[0]['attackers']:
                    if self.x['character_id'] in self.x:
                        if self.x['character_id'] == self.id:
                            self.temp = await self.esi.type_get_name(self.x['ship_type_id'])
                            return self.temp
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))
        
    async def getLastSeenDate(self):
        try:
            self.timestamp = self.response[0]['killmail_time']
            self.ts = time.strptime(self.timestamp[:19], "%Y-%m-%dT%H:%M:%S")
            self.timestamp = time.strftime("%d.%m.%Y at %H:%M:%S", self.ts)
            return self.timestamp
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))
        
    async def getLastKillmailID(self):
        try:
            return self.response[0]['killmail_id']
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))
