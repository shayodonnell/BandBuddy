from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField, DateField, SelectField, FieldList
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):
    name = StringField('First name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address.')])
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(),
            Length(min=8, message='Password must be at least 8 characters long.')
        ]
        )
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
    tag = StringField('Tag', validators=[DataRequired()])

class BandAdForm(FlaskForm):
    band = SelectField('Band', validators=[DataRequired()])
    lookingfor = StringField('Looking for', validators=[DataRequired()])
    deadline = DateField('Deadline', validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TagPreferences(FlaskForm):
    tag = StringField('Tag', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Submit')

class ProfilePictureForm(FlaskForm):
    url = StringField('Url', validators=[Length(min=5,max=100)])
    submit = SubmitField('Submit')