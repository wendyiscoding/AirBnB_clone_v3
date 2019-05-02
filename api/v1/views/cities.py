#!/usr/bin/python3
"""
creates new view for City objects that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, Response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    """Retrieves list of all Cities objects"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == 'POST':
        x = request.get_json()
        if request.is_json is False:
            return jsonify(error="Not a JSON"), 400
        if 'name' not in x.keys():
            return jsonify(error="Missing name"), 400
        x['state_id'] = state_id
        new_city = City(**x)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201
    cities = state.cities
    city_list = []
    for city in cities:
        if city.state_id == state_id:
            city_list.append(city)
    return jsonify([item.to_dict() for item in city_list]), 200


@app_views.route('/cities/<city_id>',
                 methods=['GET', 'PUT', 'DELETE'])
def city_id(city_id):
    """Retrieves a City object"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        """get_json() parses and returns the data (HTTP body) as JSON"""
        x = request.get_json()
        if request.is_json is False:
            return jsonify(error="Not a JSON"), 400
        ignore = ['id', 'created_at', 'updated_at']
        for key, value in x.items():
            if key not in ignore:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
