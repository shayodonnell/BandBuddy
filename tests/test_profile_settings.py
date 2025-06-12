import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture()
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def create_user(name="User", email="user@example.com"):
    user = User(name=name, email=email,
                password_hash=generate_password_hash("secret"))
    db.session.add(user)
    db.session.commit()
    return user

def test_profile_settings_requires_login(client):
    user = create_user()
    response = client.get(f"/profile_settings/{user.id}", follow_redirects=False)
    assert response.status_code == 302
    assert "/signin" in response.headers.get("Location", "")

def test_profile_settings_forbidden_when_wrong_user(client):
    user1 = create_user(name="User1", email="user1@example.com")
    user2 = create_user(name="User2", email="user2@example.com")
    with client.session_transaction() as sess:
        sess["logged_in"] = True
        sess["user_id"] = user2.id
    response = client.get(f"/profile_settings/{user1.id}")
    assert response.status_code == 403

