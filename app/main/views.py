import os

from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, send_from_directory, Response, jsonify
from app.controls.auth import *
from app.controls.operacoes import *
from app.controls.utils import *
from app.model.models import *
from decimal import Decimal

views = Blueprint("views", __name__)
auth = Autenticacao()
oper = Operacoes()

# Classes referentes a autenticação e regsitro no sistema
# ----------------------
@views.route('/', methods=['GET', 'POST'])
def index():
    if 'email' in session:
        return redirect(url_for('views.home'))
    else:
        return render_template('login.html', page=None)


@views.route('/home', methods=['GET', 'POST'])
def home():
    if 'email' in session:    
        nome = session.get("nome")
        dashboard = oper.getDashboard(session.get("token"))
        perfil = oper.getPerfil(session.get('token'), session.get('email'))
        return render_template('index.html', nome=nome, dashboard=dashboard, perfil=perfil)
    else:
        return render_template('login.html', page=None)

@views.route('/logout', methods=['GET'])
def sair():
    session.pop('email', None)
    session.pop('id', None)
    session.pop('nome', None)
    session.pop('token', None)
    session.pop('adm', None)
    session.pop('msg', None)
    session.pop('value', None)
    session.pop('superuser', None)
    return redirect(url_for('views.index'))

@views.route('/recuperasenha', methods=['GET'])
def recuperar_senha():
    if 'email' in session:
        return redirect(url_for('views.home'))
    else:
        return render_template('recuperasenha.html', page=None)


@views.route('/login', methods=['POST'])
def user():
    result = auth.autenticarUsuario(
        request.form['email-login'], request.form['password'])

    if 'email' in session:
        return redirect(url_for('views.home'))

    else:

        if request.method == 'POST':

            if result.get("code") == "200":
                session['email'] = result.get("email")
                session['token'] = result.get("token")
                session['nome'] = result.get("nome")
                session['id'] = result.get("id")
                session['superuser'] = result.get("superuser")
                return redirect(url_for('views.home'))
            else:
                return render_template('login.html', page=result)
        else:
            return render_template('login.html', page=result)


@views.route('/registro', methods=['GET'])
def cadastro():
    if 'email' in session:
        return redirect(url_for('views.home'))
    else:
        return render_template('registro.html', page=None)


@views.route('/perfil', methods=['GET'])
def atualizarPerfil():
    if 'email' in session:
        perfil = oper.getPerfil(session.get('token'), session.get('email'))
        return render_template('perfil.html', perfil = perfil, page=None)

    else:
        return render_template('login.html', page=None)


@views.route('/perfil/atualizar', methods=['POST'])
def atualizarUsuario():
    if 'email' in session:
        perfil = Perfil(request.values.get('id'), "", request.values.get('email'), request.values.get('nomecompleto'), request.values.get('sexo'), request.values.get('celular'), request.values.get('dtnascimento'), "", "", "","", "", "")
        result = auth.atualizarUsuario(perfil, session.get('token'))
        return result.get("code")
    
    else:
        return render_template('login.html', page=None)


@views.route('/sistemas', methods=['GET'])
@views.route('/sistemas/<id>', methods=['GET'])
def carregarSistemas(id=None):
    perfil = oper.getPerfil(session.get('token'), session.get('email'))
    
    if 'email' in session:
        if id==None:
            sistemas = oper.getSistemas(session.get('token'))
            return render_template('sistemas/sistema.html', perfil=perfil, sistemas=sistemas, page=None)
        else:    
            sistema = oper.getSistema(session.get('token'), id)
            return render_template("sistemas/sistemadetail.html", perfil=perfil, sistema=sistema, page=None)

    else:
        return render_template('login.html', page=None)
    
    
@views.route('/sistemas/novo', methods=['GET'])
def adicionarSistema():
    perfil = oper.getPerfil(session.get('token'), session.get('email'))
    
    if 'email' in session:
        sistema = Sistema('', '', '', '', '', '')
        return render_template("sistemas/sistemadetail.html", perfil=perfil, sistema=sistema, page=None)

    else:
        return render_template('login.html', page=None)
    
    

@views.route('/sistemas/registrar', methods=['POST'])
def registrarSistema():
    if 'email' in session:
        sistema = Sistema(request.values.get('id'), request.values.get('dtregistro'), request.values.get('nome'), request.values.get('descricao'), request.values.get('tipo'), request.values.get('linguagem'))
        result = oper.registrarSistema(session.get('token'), sistema)
        return result.__str__()

    else:
        return render_template('login.html', page=None)


@views.route('/logs', methods=['GET'])
@views.route('/logs/<id>', methods=['GET'])
def carregarLogs(id=None, descricao=None):
    perfil = oper.getPerfil(session.get('token'), session.get('email'))
    
    if 'email' in session:
        if id==None:
            logs = oper.getLogs(session.get('token'))
            return render_template('logs/logregistro.html', perfil=perfil, logs=logs, page=None)
        else:    
            sistema = oper.getSistema(session.get('token'), id)
            return render_template("logs/logregistrodetail.html", perfil=perfil, log=log, page=None)

    else:
        return render_template('login.html', page=None)




