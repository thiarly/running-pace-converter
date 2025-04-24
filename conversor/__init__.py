from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import time
import os
from flask_migrate import Migrate
import sqlalchemy

os.environ['TZ'] = 'America/Sao_Paulo'
time.tzset()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'b2d8e4b8f1b6e9d1b4b0c0f2d2e8f6d4'


project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
database_path = os.path.join(project_dir, 'instance', 'database.db')


if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path



database = SQLAlchemy(app)
migrate = Migrate(app, database)


from conversor import router
from conversor import models
from conversor import forms
from conversor import utils


def create_database_if_not_exists():
    engine = sqlalchemy.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sqlalchemy.inspect(engine)
    if not inspector.has_table('suplementos'):
        # Se a tabela não existe, cria a base de dados
        with app.app_context():
            database.create_all()
            print("Base de dados criada com sucesso!")
    else:
        print("Base de dados já existe!")

create_database_if_not_exists()
