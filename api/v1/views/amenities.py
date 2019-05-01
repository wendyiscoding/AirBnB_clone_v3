#!/usr/bin/python3
"""
associates urls to our blueprint
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


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """GET request: Retrieves a list of all Amenity objects
    POST request: Creates a new instance of the object
    """
    if request.method == 'POST':
        if request.is_json is False:
            return jsonify(error='Not a JSON'), 400
        http_body = request.get_json()
        if 'name' not in http_body.keys():
            return jsonify(error='Missing name'), 400
        new_amenity = Amenity(**http_body)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201

    return jsonify([amenity.to_dict() for amenity in
                    storage.all(Amenity).values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenities_id(amenity_id):
    """GET request: retrieve the amenity linked to the id
    DELETE request: Delete the object linked to the id
    PUT request: Update the object linked to the id
    """
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        if request.is_json is False:
            return jsonify(error='Not a JSON'), 400
        new_attr = request.get_json()
        for attr in new_attr.keys():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, attr, new_attr[attr])
        storage.save()
        return jsonify(amenity.to_dict()), 200
