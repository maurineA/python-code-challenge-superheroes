#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from app.models import Power, HeroPower

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
    

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify({'id': power.id, 'name': power.name, 'description': power.description})


@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404

    data = request.get_json()
    if 'description' in data:
        power.description = data['description']
        db.session.commit()
        return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
    else:
        return jsonify({'errors': ['Missing description parameter']}), 400



@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    if 'strength' not in data or 'power_id' not in data or 'hero_id' not in data:
        return jsonify({'errors': ['Missing parameters']}), 400

    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])

    if not hero or not power:
        return jsonify({'errors': ['Hero or Power not found']}), 404

    hero_power = HeroPower(hero=hero, power=power, strength=data['strength'])
    db.session.add(hero_power)
    db.session.commit()

    powers_list = [{'id': hp.power.id, 'name': hp.power.name, 'description': hp.power.description} for hp in hero.heropowers]
    return jsonify({'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers_list}), 201



if __name__ == '__main__':
    app.run(port=5555, debug = True)
