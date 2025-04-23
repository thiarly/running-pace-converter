from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import os
import sqlalchemy
import time

os.environ['TZ'] = 'America/Sao_Paulo'
time.tzset()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dd64ab2f40726b31b2dc390c9e6a0310'

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
database_path = os.path.join(project_dir, 'instance', 'database.db')

if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path

##############################################################################
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from flask_login import UserMixin

class DummyUser(UserMixin):
    def __init__(self):
        self.id = 'anon'

@login_manager.user_loader
def load_user(user_id):
    return DummyUser()
###############################################################################



db = SQLAlchemy(app)
migrate = Migrate(app, db)

from conversor import router  # importa suas rotas
from conversor.models import Suplemento

def create_database_if_not_exists():
    engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sqlalchemy.inspect(engine)
    if not inspector.has_table('suplementos'):
        with app.app_context():
            db.create_all()
            print("Base de dados criada com sucesso")
    else:
        print("Base de dados já existe")

create_database_if_not_exists()


