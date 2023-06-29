from flask import Blueprint
from src.factory import ServiceFactory
from src.routes.validation.user import user_creation_validation, user_auth_validation, list_users_validation
from src.decorators import is_owned_by_user, validate_token

user_routes = Blueprint("user", __name__, url_prefix="/user")
controller = ServiceFactory.get_user_controller()


@user_routes.route('/<int:user_id>', methods=['GET'])
@validate_token
def get(user_id):
  return controller.get(user_id)


@user_routes.route('/', methods=['GET'])
@validate_token
def listUsers():
  data = list_users_validation()
  return controller.listUsers(data)


@user_routes.route('/', methods=['POST'])
@user_routes.route('', methods=['POST'])
def create():
  # validate request
  data = user_creation_validation()
  return controller.create(data)


@user_routes.route('/auth', methods=['POST'])
def authenticate():
  # validate request
  data = user_auth_validation()
  return controller.authenticate(data)


@user_routes.route('/<int:user_id>', methods=['DELETE'])
@validate_token
@is_owned_by_user
def delete(user_id):
  return controller.delete(user_id)
