import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from app import app, db
from app.models import User

@pytest.fixture()
def app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_user_creation(app_context):
    with app_context.app_context():
        user = User(name='Test User', email='test@example.com', password='secret')
        db.session.add(user)
        db.session.commit()
        retrieved = User.query.filter_by(email='test@example.com').first()
        assert retrieved is not None
        assert retrieved.name == 'Test User'
