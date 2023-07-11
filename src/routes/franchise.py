from flask import Blueprint
from src.factory import ServiceFactory
from src.decorators import admin_route_guard, validate_token
from src.routes.validation.franchise import validate_create_request
from flask_jwt_extended import get_jwt_identity
from webargs.flaskparser import use_args

franchise_routes = Blueprint(
    "franchise",
    __name__,
    url_prefix="/franchise")
controller = ServiceFactory.get_franchise_controller()


@franchise_routes.route('/', methods=['POST'])
@franchise_routes.route('', methods=['POST'])
@validate_token
@admin_route_guard
def create():
  # validate request
  data = validate_create_request()
  user_id = (get_jwt_identity())['id']
  data = {**data, 'user_id': user_id}
  return controller.create(data)
