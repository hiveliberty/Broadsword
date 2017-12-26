#=============================================================================#
#                                                                             #
#                   empty lib for future implementation                       #
#                                                                             #
#=============================================================================#
import asyncio
import aiohttp
import logging
import json
import base64

from config import config
from lib.token import EVEToken

log = logging.getLogger(__name__)

class ESI:
    def __init__(self, auth=False, version="v2"):
        self.endpoint_url = "https://esi.tech.ccp.is/{}".format(version)
        sel.header = ""
        pass

    def __del__(self):
        pass