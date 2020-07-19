import os
import string
import json, requests

from flask import Flask, Blueprint, current_app
from app.model.models import *
from random import randrange
from app.controls.utils import *


auth = Blueprint("auth", __name__)


class Autenticacao():
    def __init__(self):
        self.authentic = {"code": "", "msg": "", "email": "", "token":"", "nome":"", "id": "", "value":"", "superuser":""}
        self.alphabets = string.digits + string.ascii_letters

    def autenticarUsuario(self, email, password):    
        self.url = current_app.config.get('URL_BASE')+"/login"        
        strlogin = '{"username":"' +email+ '", "password":"'+password+'"}'
        response = requests.post(self.url, data=strlogin)

        try:
             if response.status_code == 200:
                 # registra o token 
                 self.authentic["code"] = "200"
                 self.authentic["msg"] = "OK"
                 self.authentic["token"] = response.headers.get("Authorization")
                 self.authentic["email"] = email                 
                 self.authentic["nome"] = email                 
                 
             elif response.status_code ==403:
                 self.authentic["code"] = "403"
                 self.authentic["msg"] = "Email ou senha estão incorretos!"

             elif response.status_code ==404:
                self.authentic["code"] = "404"
                self.authentic["msg"] = "API não localizada!"

        except Exception as e:
            self.authentic["code"] = "500"
            self.authentic["msg"] = "Erro desconhecido - {}".format(e)

        return self.authentic

    # def registrarUsuario(self, usuario):
    #     # validar se usuario já existe
    #     user = self.usuario.query.filter_by(email=usuario.email).first()
    #     if user != None:
    #         self.authentic["code"] = "500"
    #         self.authentic["msg"] = "Ops! Não foi possível efetivar o registro, pois o Email já esta registrado para outro usuário!"
    #         return self.authentic

    #     # validar se celular já existe
    #     user = self.usuario.query.filter_by(
    #         fonecelular=usuario.fonecelular).first()
    #     if user != None:
    #         self.authentic["code"] = "500"
    #         self.authentic["msg"] = "Ops! Não foi possível efetivar o registro, pois o Telefone celular já esta registrado para outro usuário!"
    #         return self.authentic

    #     self.usuario.add(usuario)
    #     self.authentic["code"] = "200"
    #     self.authentic["msg"] = "Registro efetuado com sucesso!"
    #     return self.authentic
    
    # def atualizarUsuario(self, usuario):
    #     try:
    #         self.usuario = usuario
    #         self.usuario.update()

    #         self.authentic["code"] = "200"
    #         self.authentic["msg"] = "Registro atualizado com sucesso!"
    #         return self.authentic

    #     except:
    #         self.authentic["code"] = "500"
    #         self.authentic["msg"] = "Erro desconhecido"    

    def obterUsuario(self, email):
        self.user = Usuario()
        return self.user
       
    # def enviar_senha(self, email):
    #     try:
    #         # localiza o usuario    
    #         user = self.usuario.query.filter_by(email=email).first()                      
            
    #         # criar senha provisória e atualiza
    #         senha = self.gerar_string(8)
    #         user.set_password(senha)
    #         user.update()

    #         # envia senha criada
    #         send = Utils()
    #         send.send_mail(current_app, "Recuperação de Senha", email, 'mails/send_email.html', user.nomecompleto, senha)        
            
    #         # prepara o retorn
    #         self.authentic["code"] = "200"
    #         self.authentic["msg"] = "Email enviado com sucesso!"        

    #     except:
    #         self.authentic["code"] = "500"
    #         self.authentic["msg"] = "Erro desconhecido"
            
    #     return self.authentic
