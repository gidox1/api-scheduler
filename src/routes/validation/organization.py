import json
from flask import Response, abort
from src.common import APIArgument
from flask_restful import reqparse


def validate_create_request():
  parser = reqparse.RequestParser(
      argument_class=APIArgument,
      bundle_errors=True
  )
  parser.add_argument(
      'name',
      type=str,
      required=True,
      help="The name of the organization is required",
      location="json")
  parser.add_argument(
      'country',
      type=str,
      required=True,
      help="The country where the organization is situated is required",
      location="json")
  parser.add_argument(
      'city',
      type=str,
      required=True,
      help="The city where the organization is situated is required",
      location="json")
  parser.add_argument(
      'address',
      type=str,
      required=True,
      help="The address of the organization is required",
      location="json")
  parser.add_argument('org_url', type=str, required=False,
                      help="The url of the organization", location="json")
  args = parser.parse_args()
  return args


def validate_update_request():
  parser = reqparse.RequestParser(
      bundle_errors=False,
      argument_class=APIArgument,
  )
  parser.add_argument('name', type=str, help="organization name",
                      required=False, location="json", default=None)
  parser.add_argument('country', type=str, help="organization country",
                      required=False, location="json", default=None)
  parser.add_argument('city', type=str, help="organization city",
                      required=False, location="json", default=None)
  parser.add_argument('address', type=str, help="organization address",
                      required=False, location="json", default=None)
  parser.add_argument('org_url', type=str, help="organization public url",
                      required=False, location="json", default=None)
  args = parser.parse_args()
  args_dict = {key: value for key,
               value in args.items() if value is not None}

  if len(args_dict) < 1:
    res = Response(
        json.dumps({"message": "At least one property should be updated",
                   "code": 400, "status": "FAIL"}),
        mimetype="application/json",
        status=400,
    )
    return abort(res)
  return args_dict
