from app import User
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    name = StringField(label='First Name', validators=[DataRequired()])
    last = StringField(label='Last Name', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label='Register Account')
