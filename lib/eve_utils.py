#============================================================================
#Все связанное с API запросами
#TODO - переписать оповещения под ESI
#============================================================================

import asyncio
import aiohttp
import xml.etree.ElementTree as ET
import config
#import lxml

from lxml import etree
#===================================================================================

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

async def getNotifications():
    js = ""
    print("DEBUG API: %s  vcode :%s" % (config.API.keyID, config.API.vCode))
    async with aiohttp.get("https://api.eveonline.com/char/Notifications.xml.aspx?keyID=%s&vCode=%s" %(config.API.keyID, config.API.vCode)) as r:
         if r.status == 200:
             stmp = await r.text()
             root = ET.fromstring(stmp)
             for notification in root[1][0]:
                notid=notification.get('typeID')
                tmp = await getNotificationText(notid)
                print(tmp)
                print("DEBUG %s" % notid)
                if notid == '5':
                    stmp = 'ID 5'
                    return stmp
                elif notid == '7':
                    stmp = 'ID 7'
                    return stmp
                elif notid == '8':
                    stmp = 'ID 8'
                    return stmp

                js += " %s" % notification.attrib
    return 0


async def getNotificationText(notid):
    async with aiohttp.get("https://api.eveonline.com/char/NotificationTexts.xml.aspx?keyID=%s&vCode=%s&IDs=%s" %(config.API.keyID, config.API.vCode, notid)) as r:
         if r.status == 200:
             stmp = await r.text()
             #CDATA
             print(stmp)
             return stmp
             
#===================================================================================================
#Маппинг Notification ID по версии Dramiel:
#5  - кинут вар(от алли)
#7  - кинут вар(от корпы)
#8  - Вар обнулен
#10 - выставлен налог
#13 - очередной налог
#14 - выплата награды
#16 - новое письмо
#19 - изменение налога корпы
#21 - Мембер корпы ливнул
#31 - вар обнулен (#8?)
#34 - нубшип(лолчто)
#35 - выплата страховки
#41 - потеря контроля над системой
#43 - захват контроля над системой
#52 - контракт на клона разорван на станции
#54 - страховка
#57 - уничтожение джампклона
#71 - Истечение миссии
#75 - ПОС под атакой
#76 - мало топлива на посе
#88 - IHUB атакуют
#93 - Кастом атакуют
#94 - Кастом загнали
#95 - передача IHUB
#102- Предложения помощи в варе
#103- то же что и #102
#111- награда за голову
#128- Заявка на вступление в корпу
#129- заявка на вступление отклонена
#130- Заявка отозвана
#135- ESS(Анкор? Выплата?)
#138- клон активирован
#140- Отчет об убийстве
#141- то же что и #140 (или это луз?)
#147- Начало энтозиса
#148- энтозис вrлючил модуль
#149- энтозис выключил модуль
#160- энтозис удачный
#161- Ноды деклочатся
#162- ТКУ убит
#163- станка во фрипорте
#182- цитадель анкорится
#184- Циту атакуют
#185- цита онлайн
#188- Цита уничтожена
#199- доставка в цитадель
#===================================================================================================
