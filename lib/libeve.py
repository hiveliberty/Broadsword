#==============================================================================
#   Все связанное с API запросами
#
#==============================================================================

import asyncio
import aiohttp
import xml.etree.ElementTree as ET
import config
#import lxml
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
            self.api_instance = self.api.CharacterApi()
            self.api_instance.api_client.set_default_header('User-Agent', 'BroadswordBot') # Set a relevant user agent so we know which software is actually using ESI
            self.api_instance.api_client.host = "https://esi.tech.ccp.is"
            self.api_response = self.api_instance.get_characters_character_id(id)
            return self.api_response.name
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def searchCharID(self, name):
        self.categories = 'character'
        #print(name)
        #self.search = charName
        try:
            self.api_instance = self.api.SearchApi()
            self.api_response = self.api_instance.get_search(self.categories, name, datasource=self.datasource, language=self.language, strict=self.strict, user_agent=self.user_agent, x_user_agent=self.x_user_agent)
            return self.api_response.character
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    async def getCharDetails(self, id):
        try:
            self.api_instance = self.api.CharacterApi()
            self.api_instance.api_client.set_default_header('User-Agent', 'BroadswordBot') # Set a relevant user agent so we know which software is actually using ESI
            self.api_instance.api_client.host = "https://esi.tech.ccp.is"
            self.api_response = self.api_instance.get_characters_character_id(id)
            return self.api_response
        except ApiException as e:
            print("Exception when calling StatusApi->get_status: %s\n" % e)

    def corpID(corpName):
        pass

    def corpName(corpID):
        pass

    def corpDetails(corpID):
        pass

    def allianceName(allianceID):
        pass

    def systemName(systemID):
        pass

    def systemID(systemName):
        pass

    def systemDetails(systemID):
        pass

    def regionDetails(regionID):
        pass

    def apiTypeName(typeID):
        pass

    def apiTypeID(apiTypeName):
        pass

    def apiMoonName(moonID):
        pass