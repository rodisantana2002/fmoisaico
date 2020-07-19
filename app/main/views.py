import os

from flask import Flask, Blueprint, render_template, session, request, redirect, url_for, send_from_directory, Response
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
        return render_template('index.html', nome=nome)
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
        print("aqui")                    
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


# @views.route('/registro/envio', methods=['POST'])
# def registrar():
#     if 'email' in session:
#         return redirect(url_for('views.home'))
#     else:
#         usuario = Usuario()

#         usuario.nomecompleto = request.values.get('nomecompleto')
#         usuario.email = request.values.get('email')
#         usuario.fonecelular = request.values.get('celular')
#         usuario.sexo = request.values.get('sexo')
#         usuario.dtnascimento = request.values.get('dtnascimento')
#         usuario.cep = request.values.get('cep')
#         usuario.logradouro = request.values.get('logradouro')
#         usuario.numero = request.values.get('numero')
#         usuario.complemento = request.values.get('complemento')
#         usuario.bairro = request.values.get('bairro')
#         usuario.cidade = request.values.get('cidade')
#         usuario.estado = request.values.get('estado')
#         usuario.set_password(request.values.get('senha'))

#         result = auth.registrarUsuario(usuario)

#         return result.get("code")



# @views.route('/recuperasenha/envio', methods=['POST'])
# def enviar_senha():
#     result = auth.validar_email(request.form['email-recuperar'])

#     if 'email' in session:
#         return redirect(url_for('views.home'))
#     else:
#         if result.get("code") != "200":
#             # atualizar senha e enviar email
#             result = auth.enviar_senha(request.form['email-recuperar'])
#             return redirect(url_for('views.recuperar_senha'))
#         else:
#             return render_template('recuperasenha.html', page=result)




@views.route('/perfil', methods=['GET'])
def atualizarPerfil():
    if 'email' in session:
        Usuario = auth.obterUsuario(session.get('email'))
        return render_template('perfil.html', Usuario=Usuario, page=None)

    else:
        return render_template('login.html', page=None)

# @views.route('/perfil/atualizar', methods=['POST'])
# def atualizarUsuario():
#     if 'email' in session:
#         usuario = Usuario()
#         usuario = auth.obterUsuario(session.get('id'))            
        
#         usuario.nomecompleto = request.values.get('nomecompleto')
#         usuario.fonecelular = request.values.get('celular')
#         usuario.sexo = request.values.get('sexo')
#         usuario.dtnascimento = request.values.get('dtnascimento')
#         usuario.cep = request.values.get('cep')
#         usuario.logradouro = request.values.get('logradouro')
#         usuario.numero = request.values.get('numero')
#         usuario.complemento = request.values.get('complemento')
#         usuario.bairro = request.values.get('bairro')
#         usuario.cidade = request.values.get('cidade')
#         usuario.estado = request.values.get('estado')

#         result = auth.atualizarUsuario(usuario)

#         return result.get("code")
    
#     else:
#         return render_template('login.html', page=None)
    
    
# @views.route('/perfil/acesso', methods=['POST'])
# def atualizarAcesso():
#     if 'email' in session:
#         usuario = Usuario()
#         usuario = auth.obterUsuario(session.get('id'))
                    
#         senha_atual = request.values.get('senhaAtual')
        
#         if usuario.check_password(senha_atual):            
#             usuario.set_password(request.values.get('senha'))        
#             result = auth.atualizarUsuario(usuario)

#             return result.get("code")
#         else:
#             return "403"        
    
#     else:
#         return render_template('login.html', page=None)


# @views.route('/dashboard', methods=['GET'])
# @views.route('/dashboard/<status>', methods=['GET'])
# def carregarDashboard(status=None):
#     if 'email' in session:
#         usuario = auth.obterUsuario(session.get('id'))
#         if usuario.superuser=='True':
#             associados = oper.obterAssociados()
#             clientes = auth.obterClientes()
                    
#             if status==None:
#                 pedidos = oper.obterTodosPedidos()
#             else:
#                 pedidos = oper.obterPedidosDashboardByStatus(status)    
            
#             return render_template('dashboard.html', usuario=usuario, associados=associados, clientes=clientes, pedidos=pedidos)
#         else:
#             return render_template('login.html', page=None)
#     else:
#         return render_template('login.html', page=None)
    
# @views.route('/dashboard/download', methods=['GET'])    
# def gerarDownload():
#     if 'email' in session:
#         return Response(oper.obterArquivoCSV(), mimetype="text/csv", headers={"Content-disposition":"attachment; filename=dados.csv"})        
#     else:
#         return render_template('login.html', page=None)            






