from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

appInstance = Flask(__name__)
appInstance.config.from_object(Config)
db = SQLAlchemy(appInstance)
migrateInstance = Migrate(appInstance, db)
loginInstance = LoginManager(appInstance)
loginInstance.login_view = 'login'

from app import routes, models