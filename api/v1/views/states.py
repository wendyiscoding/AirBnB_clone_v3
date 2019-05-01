#!/usr/bin/python3
"""
creates new view for State objects that handles all default RestFul API actions
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


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """Retrieves list of all State objects"""
    if request.method == 'POST':
        x = request.get_json()
        if request.is_json is False:
            return jsonify(error="Not a JSON"), 400
        if 'name' not in x.keys():
            return jsonify(error="Missing name"), 400
        new_state = State(**x)
        return jsonify(new_state.to_dict()), 201
    states_dict = storage.all()
    return jsonify([item.to_dict() for item in states_dict.values()])


@app_views.route('/states/<state_id>',
                 methods=['GET', 'PUT', 'DELETE'])
def state_id(state_id):
    """Retrieves a State object"""
    if request.method != 'POST':
        state = storage.get("State", state_id)
        if state is None:
            abort(404)
        if request.method == 'GET':
            return jsonify(state.to_dict())
        if request.method == 'DELETE':
            storage.delete(state)
            return jsonify({}), 200
        if request.method == 'PUT':
            """get_json() parses and returns the data (HTTP body) as JSON"""
            x = request.get_json()
            if request.is_json is False:
                return jsonify(error="Not a JSON"), 400
            ignore = ['id', 'created_at', 'updated_at']
            for key, value in x.items():
                if key not in ignore:
                    setattr(state, key, value)
            return jsonify(state.to_dict()), 200
