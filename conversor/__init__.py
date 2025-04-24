from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Inicializa o app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dd64ab2f40726b31b2dc390c9e6a0310'

# Caminho local do banco SQLite (fallback)
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.makedirs(os.path.join(project_dir, 'instance'), exist_ok=True)
database_path = os.path.join(project_dir, 'instance', 'database.db')

# Conexão com o banco (PostgreSQL em produção, SQLite local)
db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://")  # compatibilidade com SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = db_url or f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # remove warning do SQLAlchemy

# Inicializa extensões
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importa modelos e rotas (garante registro no SQLAlchemy)
from conversor import models
from conversor import router
