from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Association table for Post and Tag (Many-to-Many)
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# Association table for User and Tag preferences (Many-to-Many)
user_tag_preferences = db.Table('user_tag_preferences',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # Relationships
    posts = db.relationship('Post', secondary=post_tags, back_populates='tags')
    users = db.relationship('User', secondary=user_tag_preferences, back_populates='tag_preferences')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(100), nullable=True)

    # Relationships
    likes = db.relationship('Like', back_populates='user', cascade='all, delete-orphan')
    interests = db.relationship('Interest', back_populates='user', cascade='all, delete-orphan')
    tag_preferences = db.relationship('Tag', secondary=user_tag_preferences, back_populates='users')
    bands = db.relationship('Band', back_populates='owner', cascade='all, delete-orphan')
    posts = db.relationship('Post', back_populates='author', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='likes')
    post = db.relationship('Post', back_populates='likes')

    # Unique Constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='_user_post_uc'),)

class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)  
    description = db.Column(db.String(500), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationships
    owner = db.relationship('User', back_populates='bands')
    bandads = db.relationship('Bandad', back_populates='band', cascade='all, delete-orphan')

class Bandad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'), nullable=False)
    lookingfor = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    band = db.relationship('Band', back_populates='bandads')
    interests = db.relationship('Interest', back_populates='ad', cascade='all, delete-orphan')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(50), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    likes = db.relationship('Like', back_populates='post', cascade='all, delete-orphan')
    author = db.relationship('User', back_populates='posts')
    tags = db.relationship('Tag', secondary=post_tags, back_populates='posts')

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_id = db.Column(db.Integer, db.ForeignKey('bandad.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', back_populates='interests')
    ad = db.relationship('Bandad', back_populates='interests')

    # Ensure a user can only register interest once per ad
    __table_args__ = (
        db.UniqueConstraint('user_id', 'ad_id', name='_user_ad_uc'),
    )
