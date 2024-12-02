from app import db

instuments = [
    "Guitar",
    "Drums",
    "Bass",
    "Vocals",
    "Keyboard",
    "Violin",
]

class BandInstruments(db.Model):
    __tablename__ = 'band_instrument'
    id = db.Column(db.Integer, primary_key = True)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'), nullable=False)
    instrument = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    band = db.relationship('Band', back_populates='instruments')
    user = db.relationship('User', back_populates='instrument_assignments')

class BandMember(db.Model):
    __tablename__ = 'BandMember'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'), primary_key=True)
    instrument = db.Column(db.String(50), nullable=False)

    user = db.relationship('User', back_populates='band_memberships')
    band = db.relationship('Band', back_populates='memberships')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)

    instrument_assignments = db.relationship('BandInstruments', back_populates='user')
    band_memberships = db.relationship('BandMember', back_populates='user')

class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50), nullable=False)  
    description = db.Column(db.String(500), nullable=True)
    
    instruments = db.relationship('BandInstruments', back_populates='band')
    memberships = db.relationship('BandMember', back_populates='band')