import json
from flask_restful import reqparse
from flask import Response, abort
from flask_restful.reqparse import Argument
from src.common import email_validator, validate_length


class APIArgument(Argument):
  def __init__(self, *args, **kwargs):
    super(APIArgument, self).__init__(*args, **kwargs)

  def handle_validation_error(self, error, bundle_errors):
    help_str = "(%s) " % self.help if self.help else ""
    msg = "[%s]: %s%s" % (self.name, help_str, str(error))
    res = Response(
        json.dumps({"message": msg, "code": 400, "status": "FAIL"}),
        mimetype="application/json",
        status=400,
    )
    return abort(res)

"""
    Validate request data for user creation
"""
def user_creation_validation():
  parser = reqparse.RequestParser(
      argument_class=APIArgument,
      bundle_errors=True)
  parser.add_argument(
      'first_name',
      type=str,
      location='json',
      required=True,
      help="First name of the user")
  parser.add_argument(
      'last_name',
      type=str,
      location='json',
      required=True,
      help="Last name of the user")
  parser.add_argument(
      'email',
      type=str,
      required=True,
      help='Email address is required',
      location='json',
      action="custom",
  )
  parser.add_argument(
      'password',
      required=True,
      type=lambda x: validate_length(
          x,
          8,
          20),
      help="User Password")
  parser.add_argument(
      'role',
      type=str,
      required=True,
      choices=(
          'ADMIN',
          'CUSTOMER',
          'SUPER_ADMIN'),
      help='Invalid role',
      location='json')
  args = parser.parse_args()
  email_validator(args['email'])
  return args

def user_auth_validation():
    parser = reqparse.RequestParser(
        argument_class=APIArgument,
        bundle_errors=True
    )
    parser.add_argument('email', type=str, location='json', help="Email is required for auth", required=True)
    parser.add_argument('password', type=str, location='json', help="Password is required", required=True)
    args = parser.parse_args()
    email_validator(args['email'])
    return args
