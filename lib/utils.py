#============================================================================
#Мусорка мини функций
#============================================================================

import asyncio

async def cmdGetParams(cmd):
    parsed = cmd.split()
    stmp = ""
    for elem in parsed:
        if elem.startswith('!'):
            continue
        if stmp != "":
            stmp += " "
        stmp += elem
    return stmp
