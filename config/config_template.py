#============================================================================
#	Config for Bot
#============================================================================
bot = {
    "token": "input your token here",
    "prefix": "!",
    "guild": "your guildID",
    "adminRoles": ["Admins", "BotAdmins"],
    "restrictedChannels": [0, 0]
}

auth = {
    "auth_url": "url",
    "exempt": ["NoAuth", "Bots"],
    "alertChannel": "",
    "periodicCheck": True,
    "periodicCheckInterval": 30,
    "nameEnforce": True,
    "corpTickers": True,    # Only works for alliances
    "setCorpRole": True,    # Only works for alliances
    "authGroups": {
        "group1": {
            "type": "",         # Only one of the two values is possible - corporation or alliance.
            "id": 0,            # Your alliance or corp id.
            "memberRole": "",   # Role must exist in your discord guild!
        }
    }
}

evemails = {
    "fromIDs": [0, 0],
    "channelID": ""
}

db = {
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": "3306",
    "database": "dbname",
    "charset": "utf8mb4",
    "connect_timeout": 5, #Don't change it if you don't know what it is for!
}

plugins = {
    "modules.admin": {
        "enabled": True,
    },
    "modules.auth": {
        "enabled": True,
    },
    "modules.eveapi": {
        "enabled": True,
    },
    "modules.queues": {
        "enabled": True,
    },
}