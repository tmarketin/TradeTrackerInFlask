from flask import Flask

appInstance = Flask(__name__)

from app import routes