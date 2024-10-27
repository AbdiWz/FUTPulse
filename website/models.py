from . import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class FUTBase(Base):
    __abstract__ = True
    ID = Column(Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    position = db.Column(db.String(150), unique=True)
    rating = db.Column(db.String(150), unique=True)
    nationality = db.Column(db.String(150), unique=True)
    club = db.Column(db.String(150), unique=True)
    price = Column(Integer)
    image_url = db.Column(db.String(150), unique=True)

    def validate_price(self):
        if int(float(self.price)) <= 0:
            raise ValueError('Price must be greater than 0!')
        
    def validate(self):
        self.validate_price()
        
    def save(self):
        self.validate()
        db.session.add(self)
        db.session.commit()

class GoldPlayers(FUTBase, db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'players'

class Icons(FUTBase, db.Model):
    __bind_key__ = 'two'
    __tablename__ = 'icons'