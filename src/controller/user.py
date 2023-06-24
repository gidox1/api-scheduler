from src.service.user.index import UserService
from src.common import extract, Result
from flask import jsonify, request


class UserController:
  def __init__(self, user_service: UserService):
    self.user_service = user_service
    pass

  """
    Gets a single user
    
    Args:
      None
    
    Returns:
      tuple: A tuple containing the JSON response and the HTTP status code.
  """
  def get(self, user_id):
    result = self.user_service.get(user_id)
    if Result.isError(result):
      return jsonify(result.error), 500
    return jsonify(result.value), 201

  """
    Creates a new user.

    Args:
      user_data (dict): A dictionary containing the user's data.

    Returns:
      tuple: A tuple containing the JSON response and the HTTP status code.
  """
  def create(self, user_data):
    data = extract(
        user_data, [
            'first_name', 'last_name', 'email', 'password', 'role'])
    result = self.user_service.create(data)
    if Result.isError(result):
      return jsonify(result.error), 500
    return jsonify(result.value), 201


  """
    Authenticate user based on provided email and password.

    Args:
      auth_data (dict): A dictionary containing the user's email and password.

    Returns:
      tuple: A tuple containing the JSON response and the HTTP status code.
  """
  def authenticate(self, auth_data):
    email, password = auth_data['email'], auth_data['password']
    result = self.user_service.authenticate(
        {"email": email, "password": password})
    if Result.isError(result):
      return jsonify(
          result.error), result.status if result.status is not None else 500
    return jsonify(result.value), 200


  """
    List users based on pagination config
    
    Args:
      filters (dict): Pagination filter config
    
    Returns:
      tuple: A tuple containing the JSON response and the HTTP status code.
  """
  def listUsers(self, filters):
    result = self.user_service.listUsers(filters)
    if Result.isError(result):
      return jsonify(
          result.error), result.status if result.status is not None else 500
    return jsonify(result.value), 200


  """
    Delete a user profile
    
    Args:
      user_id (str): The user Id to be deleted
    
    Returns:
      tuple: A tuple containing the JSON response and the HTTP status code.
  """
  def delete(self, user_id):
    result = self.user_service.delete(user_id)
    if Result.isError(result):
      return jsonify(
          result.error), result.status if result.status is not None else 500
    return jsonify(result.value), 200
