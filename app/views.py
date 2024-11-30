from flask import render_template, flash, request, redirect
from app import app, db, models
from .forms import SignupForm
import datetime

@app.route('/')
def index():
    return "Hello World!!!"

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match.', 'error')
            print("hi")
        else:
            flash('Details sent successfully.', 'success')
    return render_template('signup.html', form=form)