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
    def charName(self, charID):
        pass

    def charID(charName):
        pass

    def charDetails(charID):
        pass

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