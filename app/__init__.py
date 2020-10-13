from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

appInstance = Flask(__name__)
appInstance.config.from_object(Config)

db = SQLAlchemy(appInstance)
migrateInstance = Migrate(appInstance, db)

loginInstance = LoginManager(appInstance)
loginInstance.login_view = 'login'

bootstrapInstance = Bootstrap(appInstance)

from app import routes, models