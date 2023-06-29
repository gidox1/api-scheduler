from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request


def validate_token(func):
  @jwt_required()
  @wraps(func)
  def wrapper(*args, **kwargs):
    decoded_token = get_jwt_identity()
    request.decoded_token = decoded_token
    return func(*args, **kwargs)
  return wrapper


def is_owned_by_user(func):
  @jwt_required()
  @wraps(func)
  def wrapper(user_id, *args, **kwargs):
    decoded_token = get_jwt_identity()
    decoded_user_id = decoded_token['id']
    if user_id == decoded_user_id:
      return func(user_id, *args, **kwargs)
    return jsonify({
        "error": "You do not have sufficient privileges to access this resource."
    }), 401
  return wrapper


def admin_route_guard(func):
  @jwt_required()
  @wraps(func)
  def wrapper(org_id, *args, **kwargs):
    decoded_token = get_jwt_identity()
    if decoded_token['role'] != 'ADMIN':
      return jsonify({
          "error": "You do not have sufficient privileges to access this resource."
      }), 401
    return func(org_id, *args, **kwargs)
  return wrapper
