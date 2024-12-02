from flask import render_template, flash, request, redirect, session
from app import app, db, models
from .forms import SignupForm, SigninForm
import datetime

@app.route('/', methods=['GET'])
def feed():
    bands = models.Band.query.all()
    return render_template('index.html', bands=bands)

@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match.', 'error')
        else:
            newUser = models.User(name=form.name.data, email=form.email.data, password=form.password.data)
            db.session.add(newUser)
            db.session.commit()
            session['user_id'] = newUser.id
            session['logged_in'] = True
            return redirect('/')
    return render_template('signin-signup.html', form=form, title="Sign Up")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            session['user_id'] = user.id
            session['logged_in'] = True
            return redirect('/')
        else:
            flash('Invalid email or password.', 'error')
    return render_template('signin-signup.html', form=form, title="Sign In")