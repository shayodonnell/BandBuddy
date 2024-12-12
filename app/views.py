from flask import render_template, flash, request, redirect, session, jsonify
from app import app, db, models
import datetime, random
from .forms import SignupForm, SigninForm, EntryForm, PostForm, BandAdForm, NewPassword, TagPreferences, ProfilePictureForm

profile_pictures = [
    "https://i.postimg.cc/Nfrz5DSX/temp-Imagea-S53-L8.avif",
    "https://i.postimg.cc/sgYHJXVD/temp-Image-IJdan6.avif",
    "https://i.postimg.cc/tg9SvjTd/temp-Image-Nci-PGI.avif",
    "https://i.postimg.cc/VkQHMMPV/temp-Images9z-Hs-R.avif"
]

def get_random_profile_picture():
    return random.choice(profile_pictures)

@app.route('/', methods=['GET'])
def feed():
    matching_tag_posts = []
    if session.get('logged_in', False):
        user_id = session['user_id']
        user = models.User.query.get(user_id)
        user_tags = [tag.name for tag in user.tag_preferences]
        print(user_tags)
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
                "tags": [tag.name for tag in post.tags]
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
            "admin": bool(models.Band.query.get(bandad.band_id).owner == session['user_id']) if session.get('logged_in', False) else False
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
            "tags": [tag.name for tag in post.tags]
        }
        for post in posts
    ]
    feed_items = sorted(bandad_items + post_items, key = lambda x: x['date'], reverse=True)
    print(feed_items)
    return render_template('index.html', feed_items=feed_items, matching_tag_posts=matching_tag_posts, title="Feed")

@app.route('/like/<int:post_id>', methods=['POST'])
def toggle_like(post_id):
    if(session['logged_in'] == False):
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
    print("Hi")
    if(session['logged_in'] == False):
        return jsonify({"error": "You must be logged in to register interest in a band ad."}), 403
    
    user_id = session['user_id']
    new_interest = models.Interest(user_id=user_id, ad_id=ad_id, date=datetime.datetime.now())
    db.session.add(new_interest)
    db.session.commit()

    return jsonify({"success": True})

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
    if(session['logged_in'] == False):
        return jsonify({"error": "You must be logged in to post an ad."}), 403
    form = BandAdForm()
    user_bands = models.Band.query.filter_by(owner_id=session['user_id']).all()
    print("bands:",user_bands)
    form.band.choices = [(band.id, band.name) for band in user_bands]
    if form.validate_on_submit():
        newAd = models.Bandad(band=form.band.data, lookingfor=form.lookingfor.data, deadline=form.deadline.data, date=datetime.datetime.now())
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
        # Retrieve the tag from the form
        tag_name = form.tag.data.strip()
        
        if tag_name:
            # Check if the tag already exists
            tag = models.Tag.query.filter_by(name=tag_name).first()
            if not tag:
                # Create a new Tag if it doesn't exist
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
                db.session.flush()  # Flush to assign an ID to the tag
            
            # Create the new Post
            newPost = models.Post(
                content=form.content.data,
                image=form.image.data,
                author_id=session['user_id'],
                date=datetime.datetime.utcnow()
            )
            
            # Associate the tag with the post
            newPost.tags.append(tag)
        else:
            # If no tag is provided, create the post without tags
            newPost = models.Post(
                content=form.content.data,
                image=form.image.data,
                author_id=session['user_id'],
                date=datetime.datetime.utcnow()
            )
        
        # Add and commit the new post
        db.session.add(newPost)
        db.session.commit()
        
        flash('Post created successfully!', 'success')
        return redirect('/')
    
    return render_template('newband.html', form=form, title="New post")

@app.route('/newband', methods=['GET', 'POST'])
def createband():
    if(session['logged_in'] == False):
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
    session.clear()
    return redirect('/')

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match.', 'error')
        else:
            newUser = models.User(name=form.name.data, email=form.email.data, password=form.password.data, profile_picture=get_random_profile_picture())
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
            print(f"Username : {user.name}")
            session['user_name'] = user.name
            session['logged_in'] = True
            session['profile_picture'] = user.profile_picture
            return redirect('/')
        else:
            flash('Invalid email or password.', 'error')
    return render_template('signin-signup.html', form=form, title="Sign In")

@app.route('/profile_settings/<int:user_id>', methods=['GET', 'POST'])
def profile_settings(user_id):
    passwordForm = NewPassword()
    if passwordForm.validate_on_submit():
        print("Form validated")
        if passwordForm.password.data != passwordForm.confirm_password.data:
            flash('Passwords do not match.', 'error')
        else:
            user = models.User.query.get(user_id)
            user.password = passwordForm.password.data
            db.session.commit()
            return redirect('/')
    
    tag_items = models.Tag.query.filter(models.Tag.users.any(id=user_id)).all()
    
    tagForm = TagPreferences()
    if tagForm.validate_on_submit():
        tag = models.Tag(name=tagForm.tag.data)
        db.session.add(tag)
        db.session.commit()
        user = models.User.query.get(user_id)
        user.tag_preferences.append(tag)
        db.session.commit()
        return redirect(f'/profile_settings/{user_id}')
    else:
        print(tagForm.errors)

    pfpForm = ProfilePictureForm()
    if pfpForm.validate_on_submit():
        user = models.User.query.get(session['user_id'])
        user.profile_picture = pfpForm.url.data
        db.session.commit()
        session['profile_picture'] = user.profile_picture
        return redirect(f'/profile_settings/{user_id}')
    else:
        print(pfpForm.errors)
    return render_template('profile_settings.html', passwordForm=passwordForm, tagForm=tagForm, tag_items=tag_items, pfpForm=pfpForm, title="Profile Settings")