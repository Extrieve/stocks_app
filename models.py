from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
import os
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    last = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer, nullable=False)

    @property
    def prettier_budget(self):
        if len(str(self)) > 3:
            return f"{self.budget:,}$"
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Stocks(db.Model):
    name = db.Column(db.String)
    symbol = db.Column(db.String(5), primary_key=True)
    latest_price = db.Column(db.Float)
    average_volume = db.Column(db.Integer)
    fifty_high = db.Column(db.Float)
    fifty_low = db.Column(db.Float)
    iex_volume = db.Column(db.Integer)
    primary_exchange = db.Column(db.String(10))

    @property
    def prettier_budget(self):
        if len(str(self)) > 3:
            return f"{self.average_volume:,}"
        else:
            return f"{self.average_volume}"

    @property
    def pretty_iex(self):
        if self.iex_volume is not None:
            if len(str(self)) > 3:
                return f"{self.iex_volume:,}"
            else:
                return f"{self.iex_volume}"
        else:
            return f"None"


class Portfolios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    symbol = db.Column(db.String(5))
    user_id = db.Column(db.Integer)
    price = db.Column(db.Float)


class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String, nullable=False)
    last = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False)
