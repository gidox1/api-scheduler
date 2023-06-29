from flask import Blueprint
from src.factory import ServiceFactory
from src.decorators import admin_route_guard, validate_token
from src.routes.validation.organization import validate_create_request, validate_update_request
from flask_jwt_extended import get_jwt_identity

organization_routes = Blueprint(
    "organization",
    __name__,
    url_prefix="/organization")
controller = ServiceFactory.get_org_controller()


@organization_routes.route('/', methods=['POST'])
@organization_routes.route('', methods=['POST'])
@validate_token
def create():
  # validate request
  data = validate_create_request()
  user_id = (get_jwt_identity())['id']
  data = {**data, 'owner_id': user_id}
  return controller.create(data)


@organization_routes.route('/<int:org_id>', methods=['GET'])
@validate_token
def get(org_id):
  user_id = (get_jwt_identity())['id']
  return controller.get(org_id, user_id)


@organization_routes.route('/<int:org_id>', methods=['PATCH'])
@organization_routes.route('/<int:org_id>', methods=['PATCH'])
@validate_token
@admin_route_guard
def update(org_id):
  # validate request
  data = validate_update_request()
  user_id = (get_jwt_identity())['id']
  return controller.update(data, user_id, org_id)


@organization_routes.route('/<int:org_id>', methods=['DELETE'])
@organization_routes.route('/<int:org_id>', methods=['DELETE'])
@validate_token
@admin_route_guard
def delete(org_id):
  user_id = (get_jwt_identity())['id']
  return controller.delete(org_id, user_id)