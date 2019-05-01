#!/usr/bin/python3
"""
associates urls to our blueprint
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def city_place(city_id):
    """GET Request: Retrieves all Place objects of a city
    POST Request: Creates a new place object linked to city
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if request.method == 'POST':
        if request.is_json is False:
            return jsonify(error='Not a JSON'), 400
        entries = request.get_json()
        if 'user_id' not in entries.keys():
            return jsonify(error='Missing user_id'), 400
        user = storage.get('User', entries['user_id'])
        if user is None:
            abort(404)
        if 'name' not in entries.keys():
            return jsonify(error='Missing name'), 400
        entries['city_id'] = city_id
        new_place = Place(**entries)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201

    places = storage.all(Place)
    return jsonify([place.to_dict() for place in places.values()
                    if place.city_id == city_id])


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
def place_object(place_id):
    """GET Request: Retrieves place object with place_id
    DELETE Request: Deletes place object
    PUT Request: Update the place object
    """
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())
    elif request.method == 'PUT':
        if request.is_json is False:
            return jsonify(error='Not a JSON'), 400
        entries = request.get_json()
        ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for entry in entries:
            if entry not in ignore:
                setattr(place, entry, entries[entry])
        storage.save()
        return jsonify(place.to_dict()), 200
    elif request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
