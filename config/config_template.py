#============================================================================
#	Config for Bot
#============================================================================
bot = {
    "token": "input your token here",
    "prefix": "!",
    "guild": "your guildID",
    "adminRoles": ["", ""],
    "restrictedChannels": [0, 0]
}

auth = {
    "auth_url": "url",
    "exempt": ["", ""],
    "alertChannel": "",
    "nameEnforce": True,
    "corpTickers": True,
    "authGroups": {
        "group1": {
            "corpID": 0,
            "allianceID": 0,
            "corpMemberRole": "",
            "allyMemberRole": ""
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