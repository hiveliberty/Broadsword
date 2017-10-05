#============================================================================
#Конфиги
#============================================================================

class ApiKey:
    keyID = ""
    vCode = ""
    def __init__(self, keyID, vCode):
        self.keyID = keyID
        self.vCode = vCode

Bot_Tocken = ""
API = ApiKey("keyID","vCode")

