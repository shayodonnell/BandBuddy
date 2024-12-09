from app import db

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes')

class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)  
    description = db.Column(db.String(500), nullable=True)
    owner=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(50), nullable=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    likes = db.relationship('Like', back_populates='post', cascade='all, delete-orphan')

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('bandad.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', back_populates='interests')
    ad = db.relationship('Bandad', back_populates='interests')

class Bandad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    band = db.Column(db.Integer, db.ForeignKey('band.id'), nullable=False)
    lookingfor = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    interests = db.relationship('Interest', back_populates='ad', cascade='all, delete-orphan')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    likes = db.relationship('Like', back_populates='user', cascade='all, delete-orphan')
    interests = db.relationship('Interest', back_populates='user', cascade='all, delete-orphan')