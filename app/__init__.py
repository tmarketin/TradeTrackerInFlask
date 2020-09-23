from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

appInstance = Flask(__name__)
appInstance.config.from_object(Config)
db = SQLAlchemy(appInstance)
migrateInstance = Migrate(appInstance, db)

from app import routes, models