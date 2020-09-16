from flask import Flask
from config import Config

appInstance = Flask(__name__)
appInstance.config.from_object(Config)

from app import routes