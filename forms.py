from flask_wtf import FlaskForm
from models import User
from wtforms import StringField, SubmitField, FloatField, IntegerField, ValidationError, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already taken, try again!')

    def validate_email_address(self, email_address_to_check):
        email = User.query.filter_by(
            email=email_address_to_check.data).first()
        if email:
            raise ValidationError('Email already taken, try again!')

    username = StringField(label='Username', validators=[
                           Length(min=2, max=30), DataRequired()])
    password1 = PasswordField(label='Password', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password',
                              validators=[EqualTo('password1'), DataRequired()])
    name = StringField(label='First Name', validators=[DataRequired()])
    last = StringField(label='Last Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    budget = IntegerField(label='Budget', validators=[
                          DataRequired(), NumberRange(min=10)])
    submit = SubmitField(label='Register Account')


class LoginForm(FlaskForm):
    username = StringField(label='Username: ', validators=[DataRequired()])
    password = StringField(label='Password: ', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


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


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Stocks!')


class SellStocksForm(FlaskForm):
    submit = SubmitField(label='Sell Stocks!')


class FriendRequestForm(FlaskForm):
    submit = SubmitField(label='Friend Request!')
