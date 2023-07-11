from enum import Enum
import json
import logging
import os
import re
import bcrypt
from flask import Response, abort
from flask_restful.reqparse import Argument
from flask_restful import reqparse

"""
  True-Myth Implementation to handle result from function calls
"""


class Result:
  def __init__(self, success, value=None, error=None, status=None):
    self.success = success
    self.value = value
    self.error = error
    self.status = status

  @staticmethod
  def success(value):
    return Result(True, value=value)

  @staticmethod
  def failure(error):
    status = error['status'] if 'status' in error else 500
    return Result(False, error=error, status=status)

  @staticmethod
  def isError(result):
    if result.error:
      return True
    return False

  @staticmethod
  def isOk(result):
    if result.success:
      return True
    return False


"""
  Enums
"""


class UserStatus(Enum):
  ACTIVE = 'ACTIVE'
  INACTIVE = 'INACTIVE'


class Role(Enum):
  ADMIN = 'ADMIN'
  CUSTOMER = 'CUSTOMER'
  SUPER_ADMIN = 'SUPER_ADMIN'


"""
 Utils
"""
pluck = lambda dict, *args: (dict[arg] for arg in args)


def extract(dictionary, keys):
  return {key: dictionary[key] for key in keys}


def email_validator(email):
  regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
  if not re.match(regex, email):
    return abort(
        Response(
            json.dumps({"message": "email is invalid", "code": 400, "status": "FAIL"}),
            mimetype="application/json",
            status=400,
        )
    )


def validate_length(value, min_length, max_length):
  if len(value) < min_length or len(value) > max_length:
    raise ValueError(
        f'Invalid length. Must be between {min_length} and {max_length} characters.')
  return value


def hash_password(password) -> str:
  rounds = int(os.getenv('SALT_ROUND'))
  salt = bcrypt.gensalt(rounds=rounds)
  return bcrypt.hashpw(password.encode("utf-8"), salt)


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


def handleError(
        e: Exception,
        message: str,
        logger: logging,
        status=500) -> Result:
  logger.error(f"{message}: {repr(e)}")
  return Result.failure({
      "message": "An unexpected error occured",
      "status": status
  })
