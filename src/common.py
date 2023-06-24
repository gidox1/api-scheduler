from enum import Enum
import json
import os
import re
import bcrypt
from flask import Response, abort

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
