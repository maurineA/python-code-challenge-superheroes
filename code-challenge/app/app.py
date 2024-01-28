#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from models import db, Hero

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)



@app.route('/')
def home():
    return 'hello'

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_list = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(heroes_list)


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        powers_list = [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description} for hp in hero.heropowers]
        return jsonify({'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers_list})
    else:
        return jsonify({'error': 'Hero not found'}), 404
    

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(powers_list)



if __name__ == '__main__':
    app.run(port=5555)
