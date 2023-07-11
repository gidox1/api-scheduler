from src.common import APIArgument
from flask_restful import reqparse


def validate_admin_details(value):
  print(value, "valuevaluevalue")
  if not isinstance(value, dict):
    raise ValueError("Invalid admin_details")

  required_fields = ['first_name', 'last_name', 'email', 'password', 'role']
  missing_fields = [field for field in required_fields if field not in value]

  if missing_fields:
    error_message = f"The following fields are required in admin_details: {', '.join(missing_fields)}"
    raise ValueError(error_message)

  return value


def validate_create_request():
  parser = reqparse.RequestParser(
      argument_class=APIArgument,
      bundle_errors=True)
  parser.add_argument('country', type=str)
  parser.add_argument(
      'name',
      type=str,
      required=True,
      help='The name of the franchise is required')
  parser.add_argument(
      'city',
      type=str,
      required=False,
      help='The city of the franchise is required')
  parser.add_argument(
      'address',
      type=str,
      required=True,
      help='The address of the franchise is required')
  parser.add_argument(
      'manager_id',
      type=int,
      required=False,
      help='The id of the franchise manager is required')
  parser.add_argument(
      'org_id',
      type=int,
      required=True,
      help='The id of the organization owning the franchise is required')
  parser.add_argument(
      'admin_details',
      type=validate_admin_details,
      required=False,
      help='The admin details for the franchise')

  args = parser.parse_args()

  if args.get('admin_details') is not None:
    admin_details = args['admin_details']
    validate_admin_details(admin_details)

  return args
