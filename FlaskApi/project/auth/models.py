import sys
import os
from project import db
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, username, password, name, surname, email):
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.email = email

    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def __init__(self, jti):
        self.jti = jti


    def add(self):
        db.session.add(self)
        db.session.commit()

