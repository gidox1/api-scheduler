from src.service.user.index import UserService
from src.common import extract, Result
from flask import jsonify, request

class UserController:
  def __init__(self, user_service: UserService):
    self.user_service = user_service
    pass

  def get(self):
    users = self.user_service.get()
    return users

  def create(self, user_data):
    data= extract(user_data, ['first_name', 'last_name', 'email', 'password', 'role'])
    result = self.user_service.create(data)
    if Result.isError(result):
      return jsonify(result.error), 500
    return jsonify(result.value), 201

  def listUsers(self, user_id):
    user = self.user_service.listUsers(user_id)
    return {'user': user}
