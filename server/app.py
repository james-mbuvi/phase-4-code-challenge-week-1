from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'Welcome to the superheroes API'

class Heroes(Resource):
    def get(self):
        heroes = []
        for hero in Hero.query.all():
            hero_dict = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            }
            heroes.append(hero_dict)
        return make_response(jsonify(heroes), 200)

class HeroesId(Resource):
    def get(self, id):
        hero = Hero.query.filter(Hero.id == id).first()
        if hero:
            hero_dict = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "hero_powers": []  
            }
            for hero_power in hero.hero_power:
                power_dict = {
                    "id": hero_power.power.id,
                    "name": hero_power.power.name,
                    "description": hero_power.power.description
                }
                hero_dict["hero_powers"].append(power_dict)
            return make_response(jsonify(hero_dict), 200)
        else:
            return make_response(jsonify({"error": "Hero not found"}), 404)

class Powers(Resource):
    def get(self):
        powers = []
        for power in Power.query.all():
            power_dict = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            powers.append(power_dict)
        return make_response(jsonify(powers), 200)

class PowersId(Resource):
    def get(self, id):
        power = Power.query.filter(Power.id == id).first()
        if power:
            power_dict = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            return make_response(jsonify(power_dict), 200)
        else:
            return make_response(jsonify({"error": "Power not found"}), 404)

    def patch(self, id):
        power = Power.query.filter(Power.id == id).first()
        if not power:
            return make_response(jsonify({"error": "Power not found"}), 404)

        request_data = request.get_json()
        if 'description' in request_data:
            new_description = request_data['description']
            if len(new_description) < 20:
                return make_response(jsonify({"error": "Description should be at least 20 characters"}), 400)
            power.description = new_description
            db.session.commit()

        power_dict = {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
        return make_response(jsonify(power_dict), 200)

class HeroPower(Resource):
    def post(self):
        data = request.get_json()
        strength = data.get('strength')
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')

        if strength not in ["Strong", "Weak", "Average"]:
            return make_response(jsonify({"errors": ["Invalid strength value"]}), 400)

        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)

        if not hero or not power:
            return make_response(jsonify({"error": "Hero or Power not found"}), 404)

        new_hero_power = HeroPower(strength=strength, hero=hero, power=power)
        db.session.add(new_hero_power)
        db.session.commit()

        return make_response(jsonify(new_hero_power.to_dict()), 200)

api.add_resource(Heroes, '/heroes')
api.add_resource(HeroesId, '/heroes/<int:id>')
api.add_resource(Powers, '/powers')
api.add_resource(PowersId, '/powers/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5555)
