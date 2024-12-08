from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

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

class BandAd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    band = db.Column(db.Integer, db.ForeignKey('band.id'), nullable=False)
    lookingfor = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    date = db.Column(db.DateTime, nullable=False)