from enum import Enum

class tipo(Enum):
    Erro = "ERROR"
    Aviso = "INFO"
    Atencao = "WARNING"
    
class Sistema(Enum):    
    FrontEnd = "FRONTEND"
    BackEnd = "BACKEND"
    API = "API"
    Mobile = "MOBILE"
    Desktop = "DESKTOP"
    IOT = "IOT"


