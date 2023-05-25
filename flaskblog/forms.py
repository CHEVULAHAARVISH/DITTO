from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField ,SubmitField , BooleanField,ValidationError,SelectField
from wtforms.validators import DataRequired , Length,Email , EqualTo
from flaskblog.models import User,Mail
class RegristrtationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min = 2,max=20)])
    email = StringField("Email",validators=[
    DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    confirm_password = PasswordField("Conform Password",validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Sign up")
    
    def validate_username(self,username):
        user =User.query.filter(username==username.data).first()
        if user:
            raise ValidationError("That username is already in use")
        
    def validate_email(self,email):
        user =User.query.filter(email==email.data).first()
        if user:
            raise ValidationError("That email is already in use")    

class LoginForm(FlaskForm):
    email = StringField("Email",validators=[DataRequired(), Email()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class QrcodeForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    confirm_email = StringField("Conform Email", validators=[DataRequired(), Email(), EqualTo("email")])
    pickup_location = SelectField("Pickup Location", choices=[("SET BLOCK", " SET BLOCK"), ("MUNCHIES", " MUNCHIES")], validators=[DataRequired()])
    drop_location = SelectField("Drop Location", choices=[("MUNCHIES", " MUNCHIES"), ("SET BLOCK", " SET BLOCK")], validators=[DataRequired()])
    package = StringField("Please enter what package is been sent", validators=[DataRequired()])
    submit = SubmitField("SEND QR")
