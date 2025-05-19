# migrate.py
from main import app
from flask_migrate import upgrade

with app.app_context():
    upgrade()