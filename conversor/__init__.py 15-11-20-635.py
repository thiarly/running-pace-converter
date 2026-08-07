from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
import os
import time
import sqlalchemy

os.environ['TZ'] = 'America/Sao_Paulo'
time.tzset()

database = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b2d8e4b8f1b6e9d1b4b0c0f2d2e8f6d4'

    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    database_path = os.path.join(project_dir, 'instance', 'database.db')

    db_url = os.getenv('DATABASE_URL')
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://')

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or 'sqlite:///' + database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    database.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, database)

    from conversor import router, models, forms, utils
    app.register_blueprint(router)

    with app.app_context():
        engine = database.engine
        inspector = sqlalchemy.inspect(engine)
        if not inspector.has_table('suplementos'):
            database.create_all()
            print("Base de dados criada com sucesso!")
        else:
            print("Base de dados já existe!")

    return app
