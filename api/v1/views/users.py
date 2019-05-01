#!/usr/bin/python3
"""
creates new view for User object that handles all default RestFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """GET request: retrieves the list of all User objects
    POST request: creates a new instance of the object"""
    if request.method == 'POST':
        if request.is_json is False:
            return jsonify(error='Not a JSON'), 400
        http_body = request.get_json()
        if 'email' not in http_body.keys():
            return jsonify(error='Missing email'), 400
        if 'password' not in http_body.keys():
            return jsonify(error='Missing password'), 400
        new_user = User(**http_body)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201
    return jsonify([user.to_dict() for user in storage.all(User).values()])


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
def user_id(user_id):
    """GET request: retrieves a User object
    DELETE request: deletes a User object"""
    user = storage.get('User', user_id)
    if user is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if request.is_json is False:
            return jsonify(error='Not a JSON'), 400
        new_attr = request.get_json()
        for attr in new_attr.keys():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(user, attr, new_attr[attr])
        storage.save()
        return jsonify(user.to_dict()), 200
