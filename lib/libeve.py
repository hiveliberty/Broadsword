#==============================================================================
#   Все связанное с API запросами
#
#==============================================================================

import asyncio
import aiohttp
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import config
#import lxml
import json
from lxml import etree
from vendor import swagger_client
from vendor.swagger_client.rest import ApiException

#==============================================================================

class EVEBasic:
    async def getTQOnline():
        async with aiohttp.get('https://crest-tq.eveonline.com/') as r:
            if r.status == 200:
                js = await r.json()
                return js
    
    async def getCharInfo(name): #TODO - Развернутую стату (EVE-Kill не пашет)
        if name == "":
            return "**Использование:** !charinfo имя персонажа"
        name = name.replace(" ","%20") #Подготовить пробелы для URL (если надо)
        #print(name)
        async with aiohttp.get("https://api.eveonline.com/eve/CharacterID.xml.aspx?names=%s" % name) as r:
            if r.status == 200:
                stmp = await r.text()
                root = ET.fromstring(stmp)
                cid = root[1][0][0].get("characterID")
                if cid == "0": #Неверное имя персонажа
                    return "Неверное имя персонажа!"
                js = "https://zkillboard.com/character/%s/" % cid
                return js


class EVEApi:
    def __init__(self):
        self.api = swagger_client
        self.datasource = 'tranquility'
        self.user_agent = 'BroadswordBot'
        self.x_user_agent = self.user_agent
        self.language = 'en-us'
        self.strict = False

    async def statusTQ(self):
        try:
            self.api_instance = self.api.StatusApi()
            #self.api_response = self.api_instance.get_status(datasource=self.datasource, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            self.api_response = self.api_instance.get_status()
            return self.api_response
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getCharName(self, id):
        try:
            self.charinfo = await self.getCharDetails(id)
            return self.charinfo.name
            #self.api_instance = self.api.CharacterApi()
            #self.api_instance.api_client.set_default_header('User-Agent', 'BroadswordBot') # Set a relevant user agent so we know which software is actually using ESI
            #self.api_instance.api_client.host = "https://esi.tech.ccp.is"
            #self.api_response = self.api_instance.get_characters_character_id(id, datasource=self.datasource, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            #return self.api_response.name
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getCharID(self, name):
        self.categories = ['character']
        try:
            self.api_instance = self.api.SearchApi()
            self.api_response = self.api_instance.get_search(self.categories, name, datasource=self.datasource, language=self.language, strict=self.strict, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.character[0]
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getCharDetails(self, id):
        try:
            self.api_instance = self.api.CharacterApi()
            self.api_response = self.api_instance.get_characters_character_id(id, datasource=self.datasource, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getCorpID(self, name):
        self.categories = ['corporation']
        try:
            self.api_instance = self.api.SearchApi()
            self.api_response = self.api_instance.get_search(self.categories, name, datasource=self.datasource, language=self.language, strict=self.strict, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.character[0]
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getCorpName(self, id):
        try:
            self.corpinfo = await self.getCorpDetails(id)
            return self.corpinfo.corporation_name
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getCorpDetails(self, id):
        try:
            self.api_instance = self.api.CorporationApi()
            self.api_response = self.api_instance.get_corporations_corporation_id(id, datasource=self.datasource, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getAllianceName(self, id):
        try:
            self.api_instance = self.api.AllianceApi()
            self.api_response = self.api_instance.get_alliances_alliance_id(id, datasource=self.datasource, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.alliance_name
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getSystemName(self, id):
        try:
            self.systeminfo = await self.getSystemDetails(id)
            return self.systeminfo.name
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getSystemID(self, name):
        self.categories = ['solarsystem']
        try:
            self.api_instance = self.api.SearchApi()
            self.api_response = self.api_instance.get_search(self.categories, name, datasource=self.datasource, language=self.language, strict=self.strict, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.character[0]
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getSystemDetails(self, id):
        try:
            self.api_instance = self.api.UniverseApi()
            self.api_response = self.api_instance.get_universe_systems_system_id(id, datasource=self.datasource, language=self.language, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getRegionDetails(self, id):
        try:
            self.api_instance = self.api.UniverseApi()
            self.api_response = self.api_instance.get_universe_regions_region_id(id, datasource=self.datasource, language=self.language, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getApiTypeName(self, id):
        try:
            self.api_instance = self.api.UniverseApi()
            self.api_response = self.api_instance.get_universe_types_type_id(id, datasource=self.datasource, language=self.language, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.name
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getApiTypeID(self, name):
        self.name = urllib.parse.quote(name, safe = '')
        self.req_url = "https://www.fuzzwork.co.uk/api/typeid.php?typename={}".format(self.name)
        try:
            self.response = urllib.request.urlopen(self.req_url)
            self.jtmp = json.loads(self.response.read().decode())
            return self.jtmp['typeID']
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getApiMoonName(self, id):
        try:
            self.api_instance = self.api.UniverseApi()
            self.api_response = self.api_instance.get_universe_moons_moon_id(id, datasource=self.datasource, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.name
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

class zKillboardAPI:
    #==============================================================================
    #   https://github.com/zKillboard/zKillboard/wiki/API-(Killmails)
    #==============================================================================
    def __init__(self, id):
        self.id = id
        self.base_url = "https://zkillboard.com/api/"
        self.req_url = self.base_url + "characterID/{}/limit/1/no-items/".format(self.id)
        self.eveapi = EVEApi()
        #self.user_agent = 'BroadswordBot'

    def __del__(self):
        del self.base_url
        
    async def getLatestSystem(self):
        async with aiohttp.get(self.req_url) as self.req:
            if self.req.status == 200:
                self.jtmp = await self.req.json()
        #self.stmp = self.eveapi.getCorpName()
        return self.jtmp[0]['solar_system_id']

    async def getLastShipTypeID(self):
        async with aiohttp.get(self.req_url) as self.req:
            if self.req.status == 200:
                self.jtmp = await self.req.json()
        try:
            if self.jtmp[0]['victim']['character_id'] == self.id:
                return self.jtmp[0]['victim']['ship_type_id']
            else:
                for self.x in self.jtmp[0]['attackers']:
                    if self.x['character_id'] in self.x:
                        if self.x['character_id'] == self.id:
                            return self.x['character_id']
        except:
            return("Failed to get ship type.")
        
    async def getLastSeenDate(self):
        async with aiohttp.get(self.req_url) as self.req:
            if self.req.status == 200:
                self.jtmp = await self.req.json()
        return self.jtmp[0]['killmail_time']
        
    async def getLastKillmailID(self):
        async with aiohttp.get(self.req_url) as self.req:
            if self.req.status == 200:
                self.jtmp = await self.req.json()
        return self.jtmp[0]['killmail_id']