#============================================================================
#Мусорка мини функций
#============================================================================

import os
import asyncio
import json

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