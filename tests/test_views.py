import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from app import app, db

@pytest.fixture()
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        with app.test_client() as client:
            yield client
        db.drop_all()

def test_profile_settings_requires_login(client):
    response = client.get('/profile_settings/1')
    assert response.status_code == 302
    assert '/signin' in response.headers['Location']

def test_profile_settings_when_logged_in(client):
    with client.session_transaction() as session:
        session['logged_in'] = True
        session['user_id'] = 1
    response = client.get('/profile_settings/1')
    assert response.status_code == 200
