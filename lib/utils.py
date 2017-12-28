#============================================================================
#Мусорка мини функций
#============================================================================

import asyncio
import aiohttp
import json
import logging
import os
#import bleach
#import requests
import urllib.request
#import urllib.parse
import re
import html
import xmltodict
#from collections import OrderedDict
from operator import itemgetter
from bs4 import BeautifulSoup
#from bs4 import NavigableString

from config import config

log = logging.getLogger(__name__)


class BasicUtils:
    def bot_version():
        with open("version", encoding='utf-8') as version_file:
            version_data = json.loads(version_file.read())
        version_file.close()
        return version_data["bot_version"]

    def db_version():
        with open("version", encoding='utf-8') as version_file:
            version_data = json.loads(version_file.read())
        version_file.close()
        return version_data["db_version"]

    def load_version():
        url = "https://raw.githubusercontent.com/hiveliberty/Broadsword/master/version"
        try:
            with urllib.request.urlopen("https://raw.githubusercontent.com/hiveliberty/Broadsword/master/version") as response:
                if response.getcode() == 200:
                    data = response.read()
                    data = json.loads(data.decode())
                    return data["bot_version"]
                else:
                    return
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            for attr in ("url", "data", "response"):
                self.__dict__.pop(attr,None)

    def check_update():
        try:
            remote_version = BasicUtils.load_version()
            if remote_version is None:
                return
            local_version = BasicUtils.bot_version()
            if local_version < remote_version:
                return True
            return False
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def cmdGetParams(cmd):
        self.parsed = cmd.split()
        self.stmp = ""
        for self.elem in self.parsed:
            if self.elem.startswith('!'):
                continue
            if self.stmp != "":
                self.stmp += " "
            self.stmp += self.elem
        return self.stmp


class AuthUtils:
    async def get_auth_group_ids(self):
        self.alliance_ids = []
        for self.group_key, self.group_value in config.auth["authGroups"].items():
            self.alliance_ids.append(self.group_value["id"])
        return self.alliance_ids

    async def is_auth_exempt(self, roles):
        self.is_exempt = False
        for self.role in roles:
            if self.role.name in config.auth['exempt']:
                self.is_exempt = True
                break
        return self.is_exempt

    async def get_auth_group_values(self, allianceID):
        for self.group_key, self.group_value in config.auth["authGroups"].items():
            if self.group_value["id"] == allianceID:
                self.values = self.group_value
                del self.group_key
                del self.group_value
                break
        return self.values


class MailUtils:
    async def xml_request(url):
        #url = url.replace(" ","%20") #Подготовить пробелы для URL (если надо)
        xml_response = await aiohttp.get(url)
        if xml_response.status == 200:
            xml_response = await xml_response.text()
            return(xml_response)
        return None

    async def clean_html(raw_html):
        clean = bleach.clean(raw_html, tags=[], strip=True)
        return clean

    async def xml_to_dict(xml, type):
        try:
            if xml is None:
                return None
            if type is None:
                return None
            if type == "test":
                #data = xmltodict.parse(xml, dict_constructor=dict)
                data = xmltodict.parse(xml)
                data = data["eveapi"]["result"]["rowset"]["row"]
                data = sorted(data, key=itemgetter('@sentDate'))
                return data
            else:
                data = xmltodict.parse(xml)
            if type == "mails":
                data = data["eveapi"]["result"]["rowset"]["row"]
                data = sorted(data, key=itemgetter('@sentDate'))
            if type == "content":
                data = data["eveapi"]["result"]["rowset"]["row"]["#text"]
            return data
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))
            return None

    async def format_mailbody(txt):
        txt = txt.replace("<br>","\n")
        txt = BeautifulSoup(txt, 'html.parser')
        for tag in txt.findAll('a'):
            if re.search("^showinfo:", tag["href"]):
                tag.unwrap()
                continue
            href = tag['href']
            href = href.replace("fitting:","https://o.smium.org/loadout/dna/")
            href = href.replace("::", "\n")
            tag.replaceWith(href)
        for tag in txt.findAll(True):
            tag.unwrap()
        txt = html.unescape(str(txt))
        return txt

    # PHP like string split
    async def str_split(s, n):
        ret = []
        s = str(s)
        try:
            for i in range(0, len(s), n):
                ret.append(s[i:i+n])
            return ret
        except Exception as e:
            if config.bot["devMode"]:
                print(e)
            log.exception("An exception has occurred in {}: ".format(__name__))
