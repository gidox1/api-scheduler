from flask_restful import reqparse
from src.common import email_validator, validate_length
from src.common import APIArgument


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
  parser.add_argument(
      'phone_number',
      type=str,
      location="json",
      help="user phone number is required")
  args = parser.parse_args()
  email_validator(args['email'])
  return args


def user_auth_validation():
  parser = reqparse.RequestParser(
      argument_class=APIArgument,
      bundle_errors=True
  )
  parser.add_argument(
      'email',
      type=str,
      location='json',
      help="Email is required for auth",
      required=True)
  parser.add_argument(
      'password',
      type=str,
      location='json',
      help="Password is required",
      required=True)
  args = parser.parse_args()
  email_validator(args['email'])
  return args


def list_users_validation():
  parser = reqparse.RequestParser(
      argument_class=APIArgument,
      bundle_errors=True
  )
  parser.add_argument(
      'page',
      type=int,
      location="json",
      help="Current page",
      required=True)
  parser.add_argument(
      'per_page',
      type=int,
      location="json",
      help="The number of items per page",
      required=True)

  args = parser.parse_args()
  return args
