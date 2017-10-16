#============================================================================
#	Config for Bot
#============================================================================
bot = {
    "token": "input your token here",
    "prefix": "!",
    "guild": "your guildID",
    "auth_url": "url"
}

db = {
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": "3306",
    "database": "dbname"
}

plugins = {
    "modules.eveapi": {
        "enabled": False,
    },
    "modules.auth": {
        "enabled": False,
    },
}