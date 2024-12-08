from flask import render_template, flash, request, redirect, session
from app import app, db, models
import datetime
from .forms import SignupForm, SigninForm, EntryForm, PostForm, BandAdForm

@app.route('/', methods=['GET'])
def feed():
    bandads = models.BandAd.query.all()
    bandad_items = [
        {
            "type": "bandad",
            "band_name": models.Band.query.get(bandad.band).name,
            "lookingfor": bandad.lookingfor,
            "deadline": bandad.deadline,
            "formatted_deadline": bandad.deadline.strftime("%d %b"),
            "date": bandad.date,
            "id": bandad.id
        }
        for bandad in bandads
    ]
    posts = models.Post.query.all()
    post_items = [
        {
            "type": "post",
            "content": post.content,
            "image": post.image,
            "author": models.User.query.get(post.author).name,
            "date": post.date,
            "id": post.id
        }
        for post in posts
    ]
    feed_items = sorted(bandad_items + post_items, key = lambda x: x['date'], reverse=True)
    print(feed_items)
    return render_template('index.html', feed_items=feed_items, title="Feed")

@app.route('/newad', methods=['GET', 'POST'])
def newad():
    if(session['logged_in'] == False):
        return redirect('/signin')
    form = BandAdForm()
    if form.validate_on_submit():
        newAd = models.BandAd(band=form.band.data, lookingfor=form.lookingfor.data, deadline=form.deadline.data, date=datetime.datetime.now())
        db.session.add(newAd)
        db.session.commit()
        return redirect('/')
    return render_template('newband.html', form=form, title="New ad")

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if(session['logged_in'] == False):
        return redirect('/signin')
    form = PostForm()
    if form.validate_on_submit():
        newPost = models.Post(content=form.content.data, image=form.image.data, author=session['user_id'], date=datetime.datetime.now())
        db.session.add(newPost)
        db.session.commit()
        return redirect('/')
    return render_template('newband.html', form=form, title="New post")

@app.route('/newband', methods=['GET', 'POST'])
def createband():
    if(session['logged_in'] == False):
        return redirect('/signin')
    form = EntryForm()
    if form.validate_on_submit():
        newBand = models.Band(name=form.name.data, genre=form.genre.data, description=form.description.data, owner=session['user_id'])
        db.session.add(newBand)
        db.session.commit()
        return redirect('/')
    return render_template('newband.html', form=form, title="New band")

@app.route('/band/<int:band_id>/delete', methods=['POST','GET'])
def deleteband(band_id):
    band = models.Band.query.get_or_404(band_id)

    if session['user_id'] != band.owner:
        flash('You are not authorized to delete this band.', 'error')
        return redirect('/')
    else:
        db.session.delete(band)
        db.session.commit()
        return redirect('/')

@app.route('/band/<int:band_id>/edit', methods=['POST','GET'])
def editband(band_id):
    band = models.Band.query.get_or_404(band_id)

    if session['user_id'] != band.owner:
        flash('You are not authorised to edit this band.', 'error')
        return redirect('/')
    
    form = EntryForm(obj=band)

    if form.validate_on_submit():
        band.name = form.name.data
        band.genre = form.genre.data
        band.description = form.description.data
        db.session.commit()
        return redirect('/')

    return render_template('newband.html', form = form, band = band, title = "Edit band")

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