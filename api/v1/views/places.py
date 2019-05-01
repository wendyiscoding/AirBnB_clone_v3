#!/usr/bin/python3
"""
associates urls to our blueprint
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places')
def city_place(city_id):
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    places = storage.all(Place)
    return jsonify([place.to_dict() for place in places.values()
                    if place.city_id == city_id])
