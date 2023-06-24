from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class LoginForm (FlaskForm):
    username = StringField('Username')
    submit = SubmitField('Login')
