from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
import config

app = Flask(__name__, static_folder=os.path.abspath('static/'))
app.config.from_object(config.Config)
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

from . import routes, models
