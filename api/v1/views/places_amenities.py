#!/usr/bin/python3
"""
creates new view for the link between Place objects and Amenity objects that
handles GET, POST, PUT, DELETE
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

@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def place_id_amenities(place_id):
    """GET method: retrieve list of all Amenity objects of a Place"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    amenities = place.amenities
    return jsonify([item.to_dict() for item in amenities])

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE', 'POST'])
def place_id_amenities_amenity_id(place_id, amenity_id):
    """DELETE method: deletes an Amenity object to a Place
    POST method: links an Amenity object to a Place"""
    place = storage.get('Place', place_id)
    amenities = storage.get('Amenity', amenity_id)
    if place is None or amenities is None:
        abort(404)
    place_amenities = place.amenities
    if request.method == 'DELETE':
        for amenity in place_amenities:
            if amenity.id == amenity_id:
                print(place.amenities)
                place.amenities.remove(amenity)
                print(place.amenities)
                storage.save()
                return jsonify({}), 200
        abort(404)
