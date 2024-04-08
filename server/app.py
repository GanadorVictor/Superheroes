# app.py

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class HeroList(Resource):
    def get(self):
        heroes = Hero.query.all()
        return jsonify([hero.to_dict() for hero in heroes])

class HeroDetail(Resource):
    def get(self, id):
        hero = Hero.query.get(id)
        if hero is None:
            return make_response(jsonify({"error": "Hero not found"}), 404)
        return jsonify(hero.to_dict(include_hero_powers=True))

class PowerList(Resource):
    def get(self):
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])

class PowerDetail(Resource):
    def get(self, id):
        power = Power.query.get(id)
        if power is None:
            return make_response(jsonify({"error": "Power not found"}), 404)
        return jsonify(power.to_dict())

class PowerUpdate(Resource):
    def patch(self, id):
        power = Power.query.get(id)
        if power is None:
            return make_response(jsonify({"error": "Power not found"}), 404)
        data = request.get_json()
        if 'description' in data:
            power.description = data['description']
            try:
                db.session.commit()
                return jsonify(power.to_dict()), 200
            except:
                db.session.rollback()
                return make_response(jsonify({"errors": ["validation errors"]}), 400)
        return make_response(jsonify({"errors": ["No data provided"]}), 400)

class HeroPowerCreate(Resource):
    def post(self):
        data = request.get_json()
        if 'strength' in data and 'power_id' in data and 'hero_id' in data:
            hero_power = HeroPower(strength=data['strength'], power_id=data['power_id'], hero_id=data['hero_id'])
            try:
                db.session.add(hero_power)
                db.session.commit()
                return jsonify(hero_power.to_dict(include_hero=True, include_power=True)), 201
            except:
                db.session.rollback()
                return make_response(jsonify({"errors": ["validation errors"]}), 400)
        return make_response(jsonify({"errors": ["Missing data"]}), 400)

api.add_resource(HeroList, '/heroes')
api.add_resource(HeroDetail, '/heroes/<int:id>')
api.add_resource(PowerList, '/powers')
api.add_resource(PowerDetail, '/powers/<int:id>')
api.add_resource(PowerUpdate, '/powers/<int:id>')
api.add_resource(HeroPowerCreate, '/hero_powers')

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
