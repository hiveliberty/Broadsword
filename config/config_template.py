bot = {
    "token": "input your token here",
    "prefix": "!",
    "guild": "your guildID",
    "adminRoles": ["Admins", "BotAdmins"],
    "cleanupchannels": ["", ""],
    "log_channel": "",
    "devMode": False, # Do not turn on this
}

# Config for token lib
# Not currently used
sso = {
    "clientID": "",
    "secretKey": "",
}

notifications = {
    "channel_id": "",
    "token": "notifications_token",
    "token_expiry": 1199,
    "check_interval": 60,
    "whitelist": [
        # 'AllWarDeclaredMsg',
        # 'DeclareWar',
        # 'EntosisCaptureStarted',
        'SovCommandNodeEventStarted',
        'SovStructureDestroyed',
        'SovStructureReinforced',
        'StructureUnderAttack',
        # 'OwnershipTransferred',
        'StructureOnline',
        'StructureFuelAlert',
        'StructureAnchoring',
        'StructureServicesOffline',
        'StructureLostShields',
        'StructureLostArmor',
        # 'TowerAlertMsg',
        'StationServiceEnabled',
        'StationServiceDisabled',
        'OrbitalReinforced',
        'OrbitalAttacked',
        'SovAllClaimAquiredMsg',
        'SovStationEnteredFreeport',
        # 'AllAnchoringMsg',
        'SovAllClaimLostMsg',
        'SovStructureSelfDestructRequested',
        'SovStructureSelfDestructFinished',
        'StationConquerMsg',
        # 'notificationTypeMoonminingExtractionStarted',
        # 'MoonminingExtractionFinished',
        # 'MoonminingLaserFired',
    ],
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
# disable:  False
plugins = {
    "modules.cleanup": {
        "enabled": False,
    },
    "modules.eveapi": {
        "enabled": False,
    },
    "modules.notifications": {
        "enabled": False,
    },
}