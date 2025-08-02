from flask import render_template, flash, request, redirect, session, jsonify, get_flashed_messages
from app import app, db, models
import datetime, random
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SignupForm, SigninForm, EntryForm, PostForm, BandAdForm, NewPassword, TagPreferences, ProfilePictureForm

profile_pictures = [
    "/static/assets/taya-iv-sBr-g8wJw5k-unsplash.jpg",
    "/static/assets/temp-Image-IJdan6.avif",
    "/static/assets/temp-Image-Nci-PGI.avif",
    "/static/assets/temp-Imagea-S53-L8.avif"
]

def get_random_profile_picture():
    return random.choice(profile_pictures)

@app.route('/', methods=['GET'])
def feed():
    # Remove expired band ads before assembling the feed
    expired_ads = models.Bandad.query.filter(
        models.Bandad.deadline < datetime.datetime.utcnow()
    ).all()
    for ad in expired_ads:
        db.session.delete(ad)
    if expired_ads:
        db.session.commit()

    matching_tag_posts = []
    if session.get('logged_in', False):
        user_id = session['user_id']
        user = models.User.query.get(user_id)
        user_tags = [tag.name for tag in user.tag_preferences]
        app.logger.debug(user_tags)
        matching_tag_posts = [
            {
                "type": "post",
                "content": post.content,
                "image": post.image,
                "author": models.User.query.get(post.author_id).name,
                "date": post.date,
                "id": post.id,
                "like_count": models.Like.query.filter_by(post_id=post.id).count(),
                "liked": bool(models.Like.query.filter_by(user_id=session['user_id'], post_id=post.id).first()) if session.get('logged_in', False) else False,
                "tags": [tag.name for tag in post.tags],
                "profile_picture": models.User.query.get(post.author_id).profile_picture
            }
            for post in models.Post.query.all()
            if any(tag.name in user_tags for tag in post.tags)
        ]

    bandads = models.Bandad.query.all()
    bandad_items = [
        {
            "type": "bandad",
            "band_name": models.Band.query.get(bandad.band_id).name,
            "lookingfor": bandad.lookingfor,
            "deadline": bandad.deadline,
            "formatted_deadline": bandad.deadline.strftime("%d %b"),
            "date": bandad.date,
            "id": bandad.id,
            "interested": bool(models.Interest.query.filter_by(user_id=session['user_id'], ad_id=bandad.id).first()) if session.get('logged_in', False) else False,
            "admin": bool(models.Band.query.get(bandad.band_id).owner_id == session['user_id']) if session.get('logged_in', False) else False
        }
        for bandad in bandads
    ]

    posts = models.Post.query.all()
    post_items = [
        {
            "type": "post",
            "content": post.content,
            "image": post.image,
            "author": models.User.query.get(post.author_id).name,
            "date": post.date,
            "id": post.id,
            "like_count": models.Like.query.filter_by(post_id=post.id).count(),
            "liked": bool(models.Like.query.filter_by(user_id=session['user_id'], post_id=post.id).first()) if session.get('logged_in', False) else False,
            "tags": [tag.name for tag in post.tags],
            "profile_picture": models.User.query.get(post.author_id).profile_picture

        }
        for post in posts
    ]
    feed_items = sorted(bandad_items + post_items, key = lambda x: x['date'], reverse=True)
    app.logger.debug(feed_items)
    return render_template('index.html', feed_items=feed_items, matching_tag_posts=matching_tag_posts, title="Feed")

@app.route('/like/<int:post_id>', methods=['POST'])
def toggle_like(post_id):
    app.logger.debug(f"Route hit with post_id: {post_id}")
    if not session.get('logged_in', False):
        return jsonify({"error": "You must be logged in to like a post."}), 403
    
    user_id = session['user_id']
    existing_like = models.Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        liked=False
    else:
        new_like = models.Like(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        liked=True
    
    like_count = models.Like.query.filter_by(post_id=post_id).count()

    return jsonify({"like_count": like_count, "liked": liked})

@app.route('/band_ad/<int:ad_id>/register_interest', methods=['POST'])
def register_interest(ad_id):
    app.logger.debug("Hi")
    if not session.get('logged_in', False):
        return jsonify({"error": "You must be logged in to register interest in a band ad."}), 403
    
    user_id = session['user_id']
    existing = models.Interest.query.filter_by(user_id=user_id, ad_id=ad_id).first()
    if existing is None:
        new_interest = models.Interest(user_id=user_id, ad_id=ad_id, date=datetime.datetime.now())
        db.session.add(new_interest)
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "error": "Already registered"})

@app.route('/band_ad/<int:ad_id>/registered_interests', methods=['GET'])
def registered_interests(ad_id):
    interests = models.Interest.query.filter_by(ad_id=ad_id).all()
    interest_items = [
        {
            "user": models.User.query.get(interest.user_id).name,
            "date": interest.date.strftime("%d %b")
        }
        for interest in interests
    ]
    feed_items = sorted(interest_items, key = lambda x: x['date'], reverse=True)
    return render_template('interests.html', feed_items=feed_items, title="Interested users")

@app.route('/newbandad', methods=['GET', 'POST'])
def newad():
    if not session.get('logged_in', False):
        return jsonify({"error": "You must be logged in to post an ad."}), 403
    form = BandAdForm()
    user_bands = models.Band.query.filter_by(owner_id=session['user_id']).all()
    app.logger.debug("bands: %s", user_bands)
    form.band.choices = [(band.id, band.name) for band in user_bands]
    if form.validate_on_submit():
        newAd = models.Bandad(band_id=form.band.data, lookingfor=form.lookingfor.data, deadline=form.deadline.data, date=datetime.datetime.now())
        db.session.add(newAd)
        db.session.commit()
        return redirect('/')
    return render_template('newband.html', form=form, title="New ad")

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    if not session.get('logged_in', False):
        return redirect('/signin')
    
    form = PostForm()
    if form.validate_on_submit():
        tag_name = form.tag.data.strip()
        
        if tag_name:
            tag = models.Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
                db.session.flush()
            
            newPost = models.Post(
                content=form.content.data,
                image=form.image.data,
                author_id=session['user_id'],
                date=datetime.datetime.utcnow()
            )
            
            newPost.tags.append(tag)
        else:
            newPost = models.Post(
                content=form.content.data,
                image=form.image.data,
                author_id=session['user_id'],
                date=datetime.datetime.utcnow()
            )
        
        db.session.add(newPost)
        db.session.commit()
        
        get_flashed_messages()
        flash('Post created successfully!', 'success')
        return redirect('/')
    
    return render_template('newband.html', form=form, title="New post")

@app.route('/newband', methods=['GET', 'POST'])
def createband():
    if not session.get('logged_in', False):
        return redirect('/signin')
    form = EntryForm()
    if form.validate_on_submit():
        newBand = models.Band(name=form.name.data, genre=form.genre.data, description=form.description.data, owner_id=session['user_id'])
        db.session.add(newBand)
        db.session.commit()
        return redirect('/')
    return render_template('newband.html', form=form, title="New band")

@app.route('/band/<int:band_id>/delete', methods=['POST','GET'])
def deleteband(band_id):
    band = models.Band.query.get_or_404(band_id)

    # Verify that the current user owns the band via owner_id
    if session['user_id'] != band.owner_id:
        get_flashed_messages()
        flash('You are not authorized to delete this band.', 'error')
        return redirect('/')
    else:
        db.session.delete(band)
        db.session.commit()
        return redirect('/')

@app.route('/band/<int:band_id>/edit', methods=['POST','GET'])
def editband(band_id):
    band = models.Band.query.get_or_404(band_id)

    # Ensure only the owner can edit the band
    if session['user_id'] != band.owner_id:
        get_flashed_messages()
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
    session.clear()
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignupForm()
    if form.validate_on_submit():
        existingUser = models.User.query.filter_by(email=form.email.data).first()
        if existingUser:
            get_flashed_messages()
            flash('Email already exists.', 'error')
            return redirect('/signup')
        if form.password.data != form.confirm_password.data:
            get_flashed_messages()
            flash('Passwords do not match.', 'error')
        else:
            newUser = models.User(name=form.name.data, email=form.email.data,
                                  password_hash=generate_password_hash(form.password.data),
                                  profile_picture=get_random_profile_picture())
            db.session.add(newUser)
            db.session.commit()
            session['user_id'] = newUser.id
            session['logged_in'] = True
            session['profile_picture'] = newUser.profile_picture
            session['user_name'] = newUser.name
            return redirect('/')
    return render_template('signin-signup.html', form=form, title="Sign Up")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            app.logger.debug("Username : %s", user.name)
            session['user_name'] = user.name
            session['logged_in'] = True
            session['profile_picture'] = user.profile_picture
            return redirect('/')
        else:
            get_flashed_messages()
            flash('Invalid email or password.', 'error')
    return render_template('signin-signup.html', form=form, title="Sign In")

@app.route('/profile_settings/<int:user_id>', methods=['GET', 'POST'])
def profile_settings(user_id):
    if not session.get('logged_in', False):
        return redirect('/signin')
    if session.get('user_id') != user_id:
        return "Forbidden", 403
    passwordForm = NewPassword()
    if passwordForm.validate_on_submit():
        app.logger.debug("Form validated")
        if passwordForm.password.data != passwordForm.confirm_password.data:
            get_flashed_messages()
            flash('Passwords do not match.', 'danger')
        else:
            user = models.User.query.get(user_id)
            user.password_hash = generate_password_hash(passwordForm.password.data)
            db.session.commit()
            get_flashed_messages()
            flash('Password updated successfully!', 'success')
            return redirect('/')

    tag_items = models.Tag.query.filter(models.Tag.users.any(id=user_id)).all()

    tagForm = TagPreferences()
    if tagForm.validate_on_submit():
        tag_name = tagForm.tag.data.strip()

        tag = models.Tag.query.filter_by(name=tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
            db.session.add(tag)
            db.session.flush()
        
        user = models.User.query.get(user_id)
        if tag not in user.tag_preferences:
            user.tag_preferences.append(tag)
            db.session.commit()
            get_flashed_messages()
            flash(f"Tag '{tag_name}' added to your preferences!", "success")
        else:
            get_flashed_messages()
            flash(f"Tag '{tag_name}' is already in your preferences.", "info")
        
        return redirect(f'/profile_settings/{user_id}')
    else:
        app.logger.debug(tagForm.errors)

    pfpForm = ProfilePictureForm()
    if pfpForm.validate_on_submit():
        user = models.User.query.get(session['user_id'])
        user.profile_picture = pfpForm.url.data
        db.session.commit()
        session['profile_picture'] = user.profile_picture
        return redirect(f'/profile_settings/{user_id}')
    else:
        app.logger.debug(pfpForm.errors)

    return render_template(
        'profile_settings.html',
        passwordForm=passwordForm,
        tagForm=tagForm,
        tag_items=tag_items,
        pfpForm=pfpForm,
        title="Profile Settings"
    )
