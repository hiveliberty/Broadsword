#==============================================================================
#
#   Все связанное с API запросами
#
#==============================================================================

import asyncio
import aiohttp
import requests
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
#import xmltodict
import time
import json
#import lxml
#from lxml import etree

from config import config
from lib.utils import BasicUtils
from vendor import swagger_client
from vendor.swagger_client.rest import ApiException

#==============================================================================
#version = await getVersion()

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

    async def make_api_request(url):
        #url = url.replace(" ","%20") #Подготовить пробелы для URL (если надо)
        xml_response = await aiohttp.get(url)
        if xml_response.status == 200:
            xml_response = await xml_response.text()
            return(xml_response)
        return None

class EVEApi:
    def __init__(self):
        self.api = swagger_client
        self.datasource = 'tranquility'
        self.user_agent = 'BroadswordBot/{}'.format(BasicUtils.getVersion())
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

    async def get_mails(self, token):
        try:
            self.api_instance = self.api.MailApi()
            #self.char_id = config.credentials["api_key"]["character_id"]
            self.api_response = self.api_instance.get_characters_character_id_mail(config.credentials["api_key"]["character_id"], datasource=self.datasource, token=token, user_agent=self.user_agent, x_user_agent=self.x_user_agent).to_dict()
            return self.api_response
            #   self.api_response content:
            #       'alliance_id'
            #       'ancestry_id'
            #       'birthday'
            #       'bloodline_id'
            #       'corporation_id'
            #       'description'
            #       'faction_id'
            #       'gender'
            #       'name'
            #       'race_id'
            #       'security_status'
        except ApiException as e:
            print("Exception when calling CharacterApi->get_status: %s\n" % e)

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
            print("Exception when calling CharacterApi->get_status: %s\n" % e)

    async def getCharID(self, name):
        self.categories = ['character']
        try:
            self.api_instance = self.api.SearchApi()
            self.api_response = self.api_instance.get_search(self.categories, name, datasource=self.datasource, language=self.language, strict=self.strict, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.character[0]
        except ApiException as e:
            print("Exception when calling SearchApi->get_status: %s\n" % e)

    async def getCharDetails(self, id):
        try:
            self.api_instance = self.api.CharacterApi()
            self.api_response = self.api_instance.get_characters_character_id(id, datasource=self.datasource, user_agent=self.user_agent, x_user_agent=self.x_user_agent).to_dict()
            return self.api_response
            #   self.api_response content:
            #       'alliance_id'
            #       'ancestry_id'
            #       'birthday'
            #       'bloodline_id'
            #       'corporation_id'
            #       'description'
            #       'faction_id'
            #       'gender'
            #       'name'
            #       'race_id'
            #       'security_status'
        except ApiException as e:
            print("Exception when calling CharacterApi->get_status: %s\n" % e)

    async def getCorpID(self, name):
        self.categories = ['corporation']
        try:
            self.api_instance = self.api.SearchApi()
            self.api_response = self.api_instance.get_search(self.categories, name, datasource=self.datasource, language=self.language, strict=self.strict, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.character[0]
        except ApiException as e:
            print("Exception when calling SearchApi->get_status: %s\n" % e)

    async def getCorpName(self, id):
        try:
            self.corpinfo = await self.getCorpDetails(id)
            return self.corpinfo.corporation_name
        except ApiException as e:
            print("Exception when calling CorporationApi->get_status: %s\n" % e)

    async def getCorpDetails(self, id):
        try:
            self.api_instance = self.api.CorporationApi()
            self.api_response = self.api_instance.get_corporations_corporation_id(id, datasource=self.datasource, user_agent=self.user_agent, x_user_agent=self.x_user_agent).to_dict()
            return self.api_response
            #   self.api_response content:
            #       'alliance_id'
            #       'ceo_id'
            #       'corporation_description'
            #       'corporation_name'
            #       'creation_date'
            #       'creator_id'
            #       'faction'
            #       'member_count'
            #       'tax_rate'
            #       'ticker'
            #       'url'
        except ApiException as e:
            print("Exception when calling CorporationApi->get_status: %s\n" % e)
        finally:
            del self.api_instance
            del self.api_response

    async def getCorpDetailsTest(self, id):
        self.req_url = "https://esi.tech.ccp.is/latest/corporations/{}/?datasource=tranquility".format(id)
        try:
            self.response = urllib.request.urlopen(self.req_url)
            self.jtmp = json.loads(self.response.read().decode())
            return self.jtmp
        except ApiException as e:
            print("Exception when calling getCorpDetailsTest->get_status: %s\n" % e)

    async def getAllianceName(self, id):
        try:
            self.api_instance = self.api.AllianceApi()
            self.api_response = self.api_instance.get_alliances_alliance_id(id, datasource=self.datasource, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.alliance_name
        except ApiException as e:
            print("Exception when calling AllianceApi->get_status: %s\n" % e)

    async def getSystemName(self, id):
        try:
            self.systeminfo = await self.getSystemDetails(id)
            return self.systeminfo.name
        except ApiException as e:
            print("Exception when calling UniverseApi->get_status: %s\n" % e)

    async def getSystemID(self, name):
        self.categories = ['solarsystem']
        try:
            self.api_instance = self.api.SearchApi()
            self.api_response = self.api_instance.get_search(self.categories, name, datasource=self.datasource, language=self.language, strict=self.strict, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.solarsystem[0]
        except ApiException as e:
            print("Exception when calling SearchApi->get_status: %s\n" % e)

    async def getSystemDetails(self, id):
        try:
            self.api_instance = self.api.UniverseApi()
            self.api_response = self.api_instance.get_universe_systems_system_id(id, datasource=self.datasource, language=self.language, user_agent=self.user_agent, x_user_agent=self.x_user_agent).to_dict()
            return self.api_response
        except ApiException as e:
            print("Exception when calling UniverseApi->get_status: %s\n" % e)

    async def getRegionDetails(self, id):
        try:
            self.api_instance = self.api.UniverseApi()
            self.api_response = self.api_instance.get_universe_regions_region_id(id, datasource=self.datasource, language=self.language, user_agent=self.user_agent, x_user_agent=self.x_user_agent).to_dict()
            return self.api_response
        except ApiException as e:
            print("Exception when calling UniverseApi->get_status: %s\n" % e)

    async def getApiTypeName(self, id):
        try:
            self.api_instance = self.api.UniverseApi()
            self.api_response = self.api_instance.get_universe_types_type_id(id, datasource=self.datasource, language=self.language, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.name
        except ApiException as e:
            print("Exception when calling UniverseApi->get_status: %s\n" % e)

    async def getApiTypeID(self, name):
        self.name = urllib.parse.quote(name, safe = '')
        self.req_url = "https://www.fuzzwork.co.uk/api/typeid.php?typename={}".format(self.name)
        try:
            self.response = urllib.request.urlopen(self.req_url)
            self.jtmp = json.loads(self.response.read().decode())
            return self.jtmp['typeID']
        except ApiException as e:
            print("Exception when calling getApiTypeID->get_status: %s\n" % e)

    async def getApiMoonName(self, id):
        try:
            self.api_instance = self.api.UniverseApi()
            self.api_response = self.api_instance.get_universe_moons_moon_id(id, datasource=self.datasource, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.name
        except ApiException as e:
            print("Exception when calling UniverseApi->get_status: %s\n" % e)

class zKillboardAPI:
    #==============================================================================
    #   https://github.com/zKillboard/zKillboard/wiki/API-(Killmails)
    #==============================================================================
    def __init__(self, id):
        self.id = id
        self.user_agent = {'user-agent': 'BroadswordBot/{}'.format(BasicUtils.getVersion())}
        print(self.user_agent)
        self.base_url = "https://zkillboard.com/api/"
        self.eve_api = EVEApi()
        self.request_url = self.base_url + "characterID/{}/limit/1/no-items/".format(self.id)
        try:
            self.response = requests.get(self.request_url)
            print(self.response)
            if self.response.status_code == 200:
                self.response = self.response.json()
                print(self.response)
        except Exception as e:
            print("Exception when calling __init__: %s\n" % e)

    # This reserved method, but is not good
    async def init(self):
        try:
            async with aiohttp.get(self.request_url) as self.response:
                print(self.response)
                if self.response.status == 200:
                    self.response = await self.response.json()
                    print(self.response)
        except Exception as e:
            print("Exception when calling init: %s\n" % e)

    async def getLatestSystem(self):
        #async with aiohttp.get(self.request_url) as self.response:
        #    if self.response.status == 200:
        #        self.response = await self.response.json()
        try:
            self.temp = await self.eve_api.getSystemName(self.response[0]['solar_system_id'])
            print(self.temp)
            return self.temp
        except Exception as e:
            print("Exception when calling getLatestSystem: %s\n" % e)
            return("Ooops.")

    async def getLastShipType(self):
        try:
            if self.response[0]['victim']['character_id'] == self.id:
                self.temp = await self.eve_api.getApiTypeName(self.response[0]['victim']['ship_type_id'])
                print(self.temp)
                return self.temp
            else:
                for self.x in self.response[0]['attackers']:
                    if self.x['character_id'] in self.x:
                        if self.x['character_id'] == self.id:
                            self.temp = await self.eve_api.getApiTypeName(self.x['ship_type_id'])
                            print(self.temp)
                            return self.temp
        except Exception as e:
            print("Exception when calling getLastShipType: %s\n" % e)
            return("Ooops.")
        
    async def getLastSeenDate(self):
        try:
            self.timestamp = self.response[0]['killmail_time']
            self.ts = time.strptime(self.timestamp[:19], "%Y-%m-%dT%H:%M:%S")
            self.timestamp = time.strftime("%d.%m.%Y at %H:%M:%S", self.ts)
            print(self.timestamp)
            return self.timestamp
        except Exception as e:
            print("Exception when calling getLastSeenDate: %s\n" % e)
            return("Ooops.")
        
    async def getLastKillmailID(self):
        try:
            print(self.response[0]['killmail_id'])
            return self.response[0]['killmail_id']
        except Exception as e:
            print("Exception when calling getLastSeenDate: %s\n" % e)
            return("Ooops.")

class EVEToken:
    async def __init__(self):
        pass