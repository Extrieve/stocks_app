from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    last = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return 'Name %r' % self.id


class Stocks(db.Model):
    symbol = db.Column(db.String(5), primary_key=True)
    latest_price = db.Column(db.Float, primary_key=True)
    average_volume = db.Column(db.Integer)
    fifty_high = db.Column(db.Float)
    fifty_low = db.Column(db.Float)
    iex_volume = db.Column(db.Integer)
    primary_exchange = db.Column(db.String(10))
