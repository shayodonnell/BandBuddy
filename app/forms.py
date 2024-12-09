from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField, DateField, SelectField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EntryForm(FlaskForm):
    name = StringField('Band name', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    content = StringField('Content', validators=[DataRequired()])
    image = StringField('Image')
    submit = SubmitField('Submit')

class BandAdForm(FlaskForm):
    band = SelectField('Band', validators=[DataRequired()])
    lookingfor = StringField('Looking for', validators=[DataRequired()])
    deadline = DateField('Deadline', validators=[DataRequired()])
    submit = SubmitField('Submit')