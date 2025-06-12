import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from app import app, db
from app.models import User, Band, Bandad, Interest
import datetime
from werkzeug.security import generate_password_hash

@pytest.fixture()
def app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_user_creation(app_context):
    with app_context.app_context():
        user = User(name='Test User', email='test@example.com',
                    password_hash=generate_password_hash('secret'))
        db.session.add(user)
        db.session.commit()
        retrieved = User.query.filter_by(email='test@example.com').first()
        assert retrieved is not None
        assert retrieved.name == 'Test User'


def test_register_interest_once(app_context):
    with app_context.app_context():
        user = User(name='User1', email='user1@example.com',
                    password_hash=generate_password_hash('pw'))
        owner = User(name='Owner', email='owner@example.com',
                     password_hash=generate_password_hash('pw'))
        db.session.add_all([user, owner])
        db.session.commit()

        band = Band(name='Band', genre='Rock', description='desc', owner_id=owner.id)
        db.session.add(band)
        db.session.commit()

        ad = Bandad(band_id=band.id, lookingfor='Drummer', deadline=datetime.datetime.now(), date=datetime.datetime.now())
        db.session.add(ad)
        db.session.commit()

        client = app_context.test_client()
        with client.session_transaction() as sess:
            sess['logged_in'] = True
            sess['user_id'] = user.id

        resp1 = client.post(f'/band_ad/{ad.id}/register_interest')
        assert resp1.get_json()['success'] is True

        resp2 = client.post(f'/band_ad/{ad.id}/register_interest')
        data = resp2.get_json()
        assert data['success'] is False
        assert 'Already registered' in data['error']

        assert Interest.query.count() == 1
