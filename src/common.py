from enum import Enum
import os
import re
import bcrypt

"""
  True-Myth Implementation to handle result from function calls
"""
class Result:
  def __init__(self, success, value=None, error=None):
    self.success = success
    self.value = value
    self.error = error

  @staticmethod
  def success(value):
    return Result(True, value=value)

  @staticmethod
  def failure(error):
    return Result(False, error=error)
    
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
    return False
  return True

def validate_length(value, min_length, max_length):
  if len(value) < min_length or len(value) > max_length:
    raise ValueError(
        f'Invalid length. Must be between {min_length} and {max_length} characters.')
  return value

def hash_password(password) -> str:
  rounds = int(os.getenv('SALT_ROUND'))
  salt = bcrypt.gensalt(rounds=rounds)
  return bcrypt.hashpw(password.encode("utf-8"), salt)