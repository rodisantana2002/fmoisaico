import os
import string
import json, requests
import jsonpickle

from flask import Flask, Blueprint, current_app
from app.model.models import *
from app.controls.utils import *
from sqlalchemy import DateTime, func
from decimal import Decimal

operacoes = Blueprint("operacoes", __name__)

class Operacoes():

    def __init__(self):
        self.authentic = {"code": "", "msg": "", "email": "", "token":"", "nome":"", "id": "", "value":"", "superuser":""}

    def getDashboard(self, token):
        self.url = current_app.config.get('URL_BASE')+"/v1/dashboard"        
        headers = {'Authorization': token}
        response = requests.get(self.url, headers=headers)
        j = json.loads(response.content)
        self.dashboard = Dashboard(**j)
        return self.dashboard


    def getPerfil(self, token, email):
        self.url = current_app.config.get('URL_BASE')+"/v1/perfis"        
        headers = {'Authorization': token}
        param = {'email': email}
        
        response = requests.get(self.url, headers=headers, params=param)
        j = json.loads(response.content)
        self.perfil = Perfil(**j[0])
        return self.perfil
        
    def getSistemas(self, token):
        self.url = current_app.config.get('URL_BASE')+"/v1/sistemas"
        headers = {'Authorization': token}
        param={'pageSize':100}
        sistemas = []

        response = requests.get(self.url, headers=headers, params=param)
        j = json.loads(response.content)
        for item in j:
            sistema = Sistema(**item)
            sistemas.append(sistema)
            
        return sistemas

    def getSistema(self, token, id):
        self.url = current_app.config.get('URL_BASE')+"/v1/sistemas/"+id
        headers = {'Authorization': token}

        response = requests.get(self.url, headers=headers)
        j = json.loads(response.content)
        sistema = Sistema(**j)
           
        return sistema

    def registrarSistema(self, token, sistema):
        headers = {'Authorization': token, 'content-type':'application/json'}      


        if sistema.id == '':
            strDados =  '{"nome": "' + sistema.nome +'", "descricao": "' + sistema.descricao + '", "tipo": "'+ sistema.tipo +'", "linguagem": "'+ sistema.linguagem +'"}'                    
            self.url = current_app.config.get('URL_BASE')+"/v1/sistemas"
            response = requests.post(self.url, data=strDados, headers=headers)                
        else:

            strDados =  '{"id": ' + sistema.id + ', "dtregistro": "' + sistema.dtregistro + '", "nome": "' + sistema.nome +'", "descricao": "' + sistema.descricao + '", "tipo": "'+ sistema.tipo +'", "linguagem": "'+ sistema.linguagem +'"}'                    
            self.url = current_app.config.get('URL_BASE')+"/v1/sistemas/" + sistema.id
            response = requests.put(self.url, data=strDados, headers=headers)                
        
        try:
             if response.status_code == 200:
                 self.authentic["code"] = "200"
                 
             elif response.status_code ==400:
                 self.authentic["code"] = "400"

             elif response.status_code ==403:
                 self.authentic["code"] = "403"

             elif response.status_code ==415:
                 self.authentic["code"] = "403"

             elif response.status_code ==404:
                self.authentic["code"] = "404"

             # carrega a mensagem conforme erro detectado
             self.authentic["msg"] = response.content                

        except Exception as e:
            self.authentic["code"] = "500"
            self.authentic["msg"] = "Erro desconhecido - {}".format(e)

        return self.authentic


    def getLogs(self, token):
        self.url = current_app.config.get('URL_BASE')+"/v1/logs"
        headers = {'Authorization': token}
        param={'pageSize':100, 'sortBy':'dtregistro', 'direction':'desc'}
        logs = []

        response = requests.get(self.url, headers=headers, params=param)
        j = json.loads(response.content)
        for item in j:
            log = Logregistro(**item)
            logs.append(log)
            
        return logs
