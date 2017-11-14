#============================================================================
#Мусорка мини функций
#============================================================================

import os
import asyncio
import json
from config import config

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

def getVersion():
    with open('version', encoding='utf-8') as version_file:
        version_data = json.loads(version_file.read())
    return version_data['version']

class AuthUtils():
    async def getAuthGroupIDs(self):
        print(config.auth["authGroups"])
        self.alliance_ids = []
        for self.group_key, self.group_value in config.auth["authGroups"].items():
            self.alliance_ids.append(self.group_value["id"])
        print(self.alliance_ids)
        return self.alliance_ids

    async def isAuthExempt(self, roles):
        self.is_exempt = False
        print(config.auth['exempt'])
        print(roles)
        for self.role in roles:
            if self.role.name in config.auth['exempt']:
                self.is_exempt = True
                break
        return self.is_exempt