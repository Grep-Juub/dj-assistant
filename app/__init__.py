import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()


app = Flask(__name__)


env = os.environ.get("FLASK_ENV", "development").capitalize()  # Defaults to 'development' if not set

if env == "Development":
    app.config.from_object("config.DevelopmentConfig")
elif env == "Production":
    app.config.from_object("config.ProductionConfig")
else:
    raise ValueError(f"Unknown environment: {env}")


app.config.from_object("config.Config")
app.secret_key = app.config["SECRET_KEY"]

db.init_app(app)


from app import routes
