"""Flask app configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from environment variables."""

    FLASK_APP = 'wsgi.py'
    #FLASK_ENV = environ.get('FLASK_ENV')
    FLASK_ENV = 'development'
    #SECRET_KEY = environ.get('SECRET_KEY')
    SECRET_KEY = "JASNDhbS"
    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
