from flask import Blueprint
from src.factory import ServiceFactory

user_routes = Blueprint("user", __name__, url_prefix="/user")
controller = ServiceFactory.get_user_controller()

@user_routes.route('/', methods=['GET'])
def get():
    return controller.get()