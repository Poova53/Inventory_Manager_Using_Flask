from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "poiuytrewqASdfgHjkl"

# configuring database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///warehouse.sqlite3"
db = SQLAlchemy(app)

# Routers
from core import routes