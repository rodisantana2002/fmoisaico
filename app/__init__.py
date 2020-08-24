import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from app.main.views import views
from app.controls.auth import auth
from app.controls.operacoes import operacoes
from app.model.models import models

db = SQLAlchemy()
app_dir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.environ.get('SECRET_KEY') or 'key SigaLogs')

    app.config['URL_BASE'] = 'https://imosaico.herokuapp.com'
   
   
    app.register_blueprint(views)
    app.register_blueprint(auth)
    app.register_blueprint(models)
    app.register_blueprint(operacoes)

    bootstrap = Bootstrap(app)

    return app
