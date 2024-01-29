from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates


db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heros'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    heropowers = db.relationship('HeroPower', backref='heros')


@validates('name', 'super_name')
def validate_name(self, key, value):
        if not value:
            raise ValueError(f"{key.capitalize()} cannot be empty.")
        return value
 

class Power(db.Model):
    __tablename__ = 'powers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    heropowers = db.relationship('HeroPower', backref='powers')

    

class HeroPower(db.Model):
    __tablename__ = 'heropowers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('heros.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'))
    strength = db.Column(db.String)