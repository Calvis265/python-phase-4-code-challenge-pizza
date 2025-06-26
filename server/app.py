#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, Restaurant, RestaurantPizza, Pizza

# --- Config ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

 

@app.route("/")
def index():
    return "<h1>Pizza Code Challenge API</h1>"


class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [r.to_dict() for r in restaurants], 200

api.add_resource(Restaurants, "/restaurants")

class RestaurantById(Resource):
    def get(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        data = restaurant.to_dict()
        data["restaurant_pizzas"] = [rp.to_dict() for rp in restaurant.restaurant_pizzas]
        return data, 200

    def delete(self, id):
        restaurant = db.session.get(Restaurant, id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        db.session.delete(restaurant)
        db.session.commit()
        return "", 204

api.add_resource(RestaurantById, "/restaurants/<int:id>")

 

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [p.to_dict() for p in pizzas], 200

api.add_resource(Pizzas, "/pizzas")

 

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()

        if not all(k in data for k in ("price", "pizza_id", "restaurant_id")):
            return {"errors": ["validation errors"]}, 400

        try:
            rp = RestaurantPizza(
                price=data["price"],
                pizza_id=data["pizza_id"],
                restaurant_id=data["restaurant_id"]
            )
            db.session.add(rp)
            db.session.commit()
            return rp.to_dict(), 201

        except Exception:
            db.session.rollback()
            return {"errors": ["validation errors"]}, 400

api.add_resource(RestaurantPizzas, "/restaurant_pizzas")

# --- Runner ---
if __name__ == "__main__":
    app.run(port=5555, debug=True)
