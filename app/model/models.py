import os
import datetime

from enum import Enum
from flask import Flask, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash

models = Blueprint("models", __name__)

app = Flask(__name__)

# Classe Perfil
class Perfil:   
    def __init__(self, id, dtregistro, email, nomecompleto, sexo, fonecelular, dtnascimento, logradouro, numero, complemento, cidade, estado, cep):
        self.id=id
        self.dtregistro = dtregistro
        self.email=email
        self.nomecompleto=nomecompleto
        self.sexo=sexo
        self.fonecelular=fonecelular
        self.dtnascimento=dtnascimento
        
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.cidade = cidade
        self.estado = estado
        self.cep = cep


class Dashboard:
    def __init__(self, totalSistemas, totalGeralLogs, totalPorSistema, totalPorTipo):
        self.totalSistemas=totalSistemas
        self.totalGeralLogs=totalGeralLogs        
        self.totalPorSistema=totalPorSistema
        self.totalPorTipo=totalPorTipo

    def getSistemas(self):        
        result=[]
        
        for key, item in self.totalPorSistema.items():
            if item>0:
                sistema = {"nome":key, "total":item, "percentual": (item/self.totalGeralLogs)*100}                        
                result.append(sistema)    

        return result


class Sistema:
    def __init__(self, id, dtregistro, nome, descricao, tipo, linguagem):
        self.id = id
        self.dtregistro = dtregistro
        self.nome = nome 
        self.descricao = descricao
        self.tipo = tipo
        self.linguagem = linguagem

class Logregistro:
    def __init__(self, id, dtregistro, tipo, descricao, qtde, sistema, log=None):
        self.id = id
        self.dtregistro = dtregistro
        self.tipo = tipo
        self.descricao = descricao
        self.qtde = qtde
        self.log = log
        self.sistema = sistema
