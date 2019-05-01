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


@app_views.route('/status')
def status():
    """Return status = OK"""
    return jsonify(status='OK')


@app_views.route('/stats')
def stats():
    """Return number of each objects by type"""
    dict_types = {"amenities": Amenity, "cities": City, "places": Place,
                  "reviews": Review, "states": State, "users": User}
    for key, values in dict_types.items():
        dict_types[key] = storage.count(values)
    return jsonify(dict_types)
