#!/usr/bin/python3
"""
creates new view for Review objects that handles GET, POST, PUT, DELETE
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


@app_views.route('places/<place_id>/reviews', methods=['GET', 'POST'])
def place_id_reviews(place_id):
    """GET method: retrieve list of all Review objects of a Place"""
    if request.method == 'POST':
        if request.is_json is False:
            abort(404)
        http_body = request.get_json()
        if "user_id" not in http_body.keys():
            return jsonify(error="Missing user_id"), 400
        user = storage.get('User', http_body['user_id'])
        if user is None:
            abort(404)
        if "text" not in http_body.keys():
            return jsonify(error="Missing text"), 400
        http_body['place_id'] = place_id
        new_review = Review(**http_body)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    reviews = storage.all('Review').values()
    reviews_list = []
    for review in reviews:
        if review.place_id == place_id:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def review_id(review_id):
    """GET method: retrive a Review object
    DELETE method: deletes a Review object
    PUT method: updates a Review object"""
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        http_body = request.get_json()
        if http_body.is_json is False:
            return jsonify(error="Not a JSON"), 400
        ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key in http_body.keys():
            if key not in ignore:
                setattr(review, key, http_body[key])
        storage.save()
        return jsonify(review.to_dict()), 200
