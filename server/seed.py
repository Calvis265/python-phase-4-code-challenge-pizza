#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    # Clear old data
    print("Deleting existing data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

     
    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="123 Karen St")
    bistro = Restaurant(name="Sanjay's Pizza Bistro", address="456 Sanjay Ave")
    palace = Restaurant(name="Kiki's Pizza Palace", address="789 Kiki Blvd")
    restaurants = [shack, bistro, palace]

    
    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    pizzas = [cheese, pepperoni, california]

    # Create restaurant-pizza relationships
    print("Creating restaurant pizzas...")
    rp1 = RestaurantPizza(price=1, restaurant=shack, pizza=cheese)
    rp2 = RestaurantPizza(price=4, restaurant=bistro, pizza=pepperoni)
    rp3 = RestaurantPizza(price=5, restaurant=palace, pizza=california)
    restaurant_pizzas = [rp1, rp2, rp3]

  
    db.session.add_all(restaurants)
    db.session.add_all(pizzas)
    db.session.add_all(restaurant_pizzas)
    db.session.commit()

    print("Seeding done!")
