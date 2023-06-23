from flask import Blueprint
from src.factory import ServiceFactory
from src.routes.validations import user_creation_validation, user_auth_validation

user_routes = Blueprint("user", __name__, url_prefix="/user")
controller = ServiceFactory.get_user_controller()


@user_routes.route('/', methods=['GET'])
def get():
  return controller.get()


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
