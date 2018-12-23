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
import time
from datetime import datetime
#from collections import OrderedDict
from operator import itemgetter
from bs4 import BeautifulSoup
#from bs4 import NavigableString

from config import config
from lib.db import DBMain

log = logging.getLogger(__name__)


class BasicUtils:
    async def eve_timestamp_convert(self, timestamp):
        # return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M:%S')
        converted = time.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S")
        converted = time.strftime("%d.%m.%Y %H:%M:%S", converted)
        return converted

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

class EVEUtils:
    # async def convert_timestamp(timestamp):
    async def timestamp_to_date(timestamp):
        converted = time.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S")
        converted = time.strftime("%d.%m.%Y %H:%M:%S", converted)
        return converted

    async def epoch_to_date(microseconds):
        seconds = microseconds/10000000 - 11644473600
        converted = datetime.utcfromtimestamp(seconds)
        converted = time.strftime("%d.%m.%Y %H:%M:%S", converted)
        return converted

    async def duration_to_date(timestamp, microseconds):
        seconds = microseconds/10000000
        converted = time.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S")
        converted = converted + datetime.timedelta(seconds=seconds)
        return time.strftime('%d.%m.%Y %H:%M:%S', converted)

    async def conv_to_percentage(value):
        if value <= 1:
            value = value * 100
        return '%.1f%%' % value


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
            log.exception("An exception has occurred in {}: ".format(__name__))

class UserdbUtils:
    async def _selfclean(self, vars):
        for attr in vars: self.__dict__.pop(attr,None)

    async def _make_id_list(self):
        self.list = []
        for self.member in self.members:
            self.list.append(self.member["discord_id"])

    async def member_id_list(self):
        try:
            self.cnx = DBMain()
            self.members = await self.cnx.member_select_all()
            await self._make_id_list()
            return self.list
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))
        finally:
            await self._selfclean(("cnx", "members", "member", "list"))
