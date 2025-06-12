import os

WTF_CSRF_ENABLED = True

# Allow configuration via environment variables with sensible defaults
SECRET_KEY = os.environ.get('SECRET_KEY', 'huak-tuah')

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SQLALCHEMY_DATABASE_URI',
    'sqlite:///' + os.path.join(basedir, 'app.db'),
)

# SQLALCHEMY_TRACK_MODIFICATIONS expects a boolean. Environment variables are
# read as strings so we perform a simple conversion with "False" as default.
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
    'SQLALCHEMY_TRACK_MODIFICATIONS', 'False'
).lower() in ('true', '1', 't', 'yes')
