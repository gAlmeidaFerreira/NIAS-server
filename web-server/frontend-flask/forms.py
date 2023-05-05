from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.simple import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class Resgistrationform(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

class LogInform(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField ("Remember me")
    submit = SubmitField("LogIn")
