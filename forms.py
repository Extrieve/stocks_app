from app import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    name = StringField(label='First Name', validators=[DataRequired()])
    last = StringField(label='Last Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Register Account')


class StocksForm(FlaskForm):
    symbol = StringField(label='Ticker Symbol', validators=[DataRequired()])
    latest_price = FloatField(label='Latest Price',
                              validators=[DataRequired()])
    average_volume = IntegerField(
        label='Average Trading Volume', validators=[DataRequired()])
    fifty_high = FloatField(label='Fifty Two Week High',
                            validators=[DataRequired()])
    fifty_low = FloatField(label='Fifty Two Week Low',
                           validators=[DataRequired()])
    iex_volume = IntegerField(label='Latest Price',
                              validators=[DataRequired()])
    primary_exchange = StringField(
        label='Trading Market', validators=[DataRequired()])
