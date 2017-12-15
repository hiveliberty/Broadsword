#============================================================================
#	Config for Bot
#============================================================================

bot = {
    "checkUpdates" : True,
    "token": "input your token here",
    "prefix": "!",
    "guild": "your guildID",
    "adminRoles": ["Admins", "BotAdmins"],
    "restrictedChannels": [0, 0],
    "devMode": False, # Do not turn on this
}

# Config for 'modules.auth'
#   'noAuthKick' - kick from guild, if member was not authorized during the one day
#   'kickWhenLeaving' - immediately kick from guild, if member leave your alliance or corporation
#   Auth Groups:
#       'type' - two values is possible: "corporation" or "alliance"
#       'id' - is your alliance or corporation ID.
#       'memberRole' - role for authorized members. Must exist in your discord guild!
#       'setCorpRole' and 'corpTickers' only works if 'type' is set to "alliance".
#
# enable:   True
# disbale:  False
auth = {
    "auth_url": "url",
    "exempt": ["NoAuth", "Bots"],
    "alertChannel": "",
    "periodicCheck": True,
    "periodicCheckInterval": 1800,
    "noAuthKick": False,
    "kickWhenLeaving": False,
    "nameEnforce": True,
    "authGroups": {
        "group1": {
            "type": "",
            "id": 0,
            "memberRole": "",
            "setCorpRole": True,
            "corpTickers": True,
            "corpColour": 0x1f8b4c,
        }
    }
}

# Config for token lib
# Not currently used
sso = {
    "character_id": 0,
    "clientID": "",
    "secretKey": "",
    "token_expiry": 1199,
}

# Config for 'modules.mail'
evemails = {
    "fromIDs": ["0",],
    "channelID": "",
    "keyID": "",
    "vCode": "",
    "characterID": 0
    "check_interval": 300,
}

# Config for database
db = {
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": "3306",
    "database": "dbname",
    "charset": "utf8mb4",
    "connect_timeout": 5, #Don't change it if you don't know what it is for!
}

# Some modules disabled by default.
# You must configure the modules that you want and enable them.
# enable:   True
# disbale:  False
plugins = {
    "modules.auth": {
        "enabled": False,
    },
    "modules.eveapi": {
        "enabled": True,
    },
    "modules.mail": {
        "enabled": False,
    },
}