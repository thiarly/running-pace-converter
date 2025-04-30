from flask import Flask, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import time
import os
from flask_migrate import Migrate
import sqlalchemy
from flask_wtf.csrf import CSRFProtect

# Configurar fuso horário
os.environ['TZ'] = 'America/Sao_Paulo'
time.tzset()

# Inicializar app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'b2d8e4b8f1b6e9d1b4b0c0f2d2e8f6d4'
csrf = CSRFProtect(app)

# Configurar banco de dados
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
database_path = os.path.join(project_dir, 'instance', 'database.db')

if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path

# Inicializar extensões
database = SQLAlchemy(app)
migrate = Migrate(app, database)
bcrypt = Bcrypt(app)

# LOGIN MANAGER novo
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # nome da função da rota de login
login_manager.login_message = "Você precisa estar logado para acessar esta página. Faça login ou cadastre-se gratuitamente."
login_manager.login_message_category = "info"


@login_manager.unauthorized_handler
def unauthorized():
    flash("🔒 Você precisa estar logado para acessar esta página. Faça login ou cadastre-se gratuitamente.", "info")
    return redirect(url_for('login', next=request.path))

# Importações internas
from conversor import router
from conversor import models
from conversor import forms
from conversor import utils

# Função para criar o banco caso não exista
def create_database_if_not_exists():
    engine = sqlalchemy.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sqlalchemy.inspect(engine)
    if not inspector.has_table('suplementos'):
        with app.app_context():
            database.create_all()
            print("Base de dados criada com sucesso!")
    else:
        print("Base de dados já existe!")

create_database_if_not_exists()