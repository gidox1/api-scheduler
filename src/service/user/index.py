import json
import logging

from sqlalchemy.exc import IntegrityError
from db import get_session
from src.model.user import User
from src.common import Result, hash_password
from src.mapper import map_user_data

class UserService:
  def __init__(self, logger: logging.Logger):
    self.logger = logger
    pass

  def get(self):
    self.logger.info('fetching users')
    return {'users': "users here"}

  def create(self, data):
    self.logger.info(f"creating user account with email {data['email']}")
    
    try:
      with get_session() as session:
        hashed_password = hash_password(data['password'])
        data["password"] = hashed_password
        user = User(**data)
        session.add(user)
        session.commit()

        return Result.success({
          "message": "user created successfully",
          "data": map_user_data(user)
        })
    except IntegrityError as e:
      self.logger.error(f"Error creating user: {str(e)}")
      return Result.failure({
          "error": "Failed to create user. User already exist.",
      })
    except Exception as e:
      self.logger.error(f"Error creating user: {str(e)}")
      return Result.failure({
        "error": "An error occurred while creating the user. Please try again later."
      })



  def listUsers(self):
    return {'user': 'user'}
