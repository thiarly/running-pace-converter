from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import sqlalchemy


app = Flask(__name__)


project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.makedirs(os.path.join(project_dir, 'instance'), exist_ok=True)  # Garante que a pasta existe
database_path = os.path.join(project_dir, 'instance', 'database.db')


db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://")  # compatibilidade com SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///' + database_path


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from conversor import models  # Importa os modelos para garantir que estão registrados no SQLAlchemy

def create_database_if_not_exists():
    engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sqlalchemy.inspect(engine)
    if not inspector.has_table('suplementos'):
        with app.app_context():
            db.drop_all()
            db.create_all()
            print("Base de dados criada com sucesso")
    else:
        print("Base de dados já existe")

create_database_if_not_exists()


