from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s:%(name)s:%(message)s"
)

app = Flask(__name__)
app.config.from_object('config')
app.logger.setLevel(logging.DEBUG)
db = SQLAlchemy(app)
# Handles all migrations.
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

from app import views, models

