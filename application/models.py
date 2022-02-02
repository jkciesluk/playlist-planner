from . import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__ = 'user'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(100),
        nullable=False,
        unique=False
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    created_on = db.Column(
        db.DateTime,
        index=False,
        unique=False,
        nullable=True
    )
    token = db.relationship("Token", backref='owner', uselist=False)
    
    # Create hashed password.
    def set_password(self, password):    
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    # Check hashed password.
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=True
    )
    expiration = db.Column(
        db.DateTime,
        primary_key=False,
        unique=False,
        nullable=True
    )
    refresh_token = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=True
    )
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id')
    )
