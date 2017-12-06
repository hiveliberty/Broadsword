#============================================================================
#	Config for Bot
#============================================================================
bot = {
    "checkUpdates" : True,
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
    "periodicCheckInterval": 1800,
    "kickWhenLeaving": True,    # Kick member when his left corp\alliance
    "nameEnforce": True,
    "authGroups": {
        "group1": {
            "type": "",         # Only one of the two values is possible - corporation or alliance.
            "id": 0,            # Your alliance or corp id.
            "memberRole": "",   # Role must exist in your discord guild!
            "setCorpRole": True,    # Only works for alliances
            "corpTickers": True,    # Only works for alliances
            "corpColour": "",
        }
    }
}

evemails = {
    "fromIDs": ["0",],
    "channelID": "",
    "keyID" => "",
    "vCode" => "",
    "characterID" => 0
}

db = {
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": "3306",
    "database": "dbname",
    "charset": "utf8mb4",
    "connect_timeout": 5, #Don't change it if you don't know what it is for!
#    "use_unicode": True,
#    "get_warnings": True,
#    "raise_on_warnings": "True",
}

plugins = {
    "modules.auth": {
        "enabled": True,
    },
    "modules.eveapi": {
        "enabled": True,
    },
    "modules.mail": {
        "enabled": False,
    },
    "modules.test": {
        "enabled": True,
    },
}