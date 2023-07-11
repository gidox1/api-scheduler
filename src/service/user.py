from typing import Dict
import logging

from sqlalchemy.exc import IntegrityError, NoResultFound
from db import get_session
from src.models import User, verify_password
from src.common import Result, hash_password
from src.mapper import map_user_data
from flask_jwt_extended import create_access_token
from datetime import timedelta


class UserService:
  def __init__(self, logger: logging.Logger):
    self.logger = logger
    pass

  def get(self, _id):
    try:
      with get_session() as session:
        user = session.query(User).filter_by(id=_id).one()
        self.logger.info(f'Retrieved user successfully: {_id}')
        return Result.success({
            "message": "user retrieved successfully",
            "data": map_user_data(user)
        })
    except NoResultFound:
      self.logger.error(f'User does not exist')
      return Result.failure({
          "message": "User not found",
          "status": 404
      })
    except Exception as e:
      self.logger.error(f"Error fetching user: {repr(e)}")
      return Result.failure({
          "error": "An error occurred while fetching user. Please try again later."
      })

  def create(self, data) -> Result:
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

  def authenticate(self, data: Dict[str, str]) -> Result:
    email = data['email']
    password = data['password']

    try:
      with get_session() as session:
        user: User = session.query(User).filter_by(email=email).one()

        if verify_password(password, user.password):
          access_token = create_access_token(
              identity={
                  "email": user.email,
                  "id": user.id,
                  "role": str(user.role.value)
              },
              expires_delta=timedelta(hours=1)
          )
          self.logger.info(f'User authenticated: {user.email}')
          return Result.success({
              "message": "User authentication successful",
              "access_token": access_token
          })
        else:
          self.logger.error(
              f'Invalid credentials for user: {user.email}')
          return Result.failure({
              "message": "Invalid credentials",
              "status": 401
          })
    except NoResultFound:
      self.logger.error(f'User does not exist: data({email})')
      return Result.failure({
          "message": "User not found",
          "status": 404
      })
    except Exception as e:
      self.logger.error(f'An unexpected error occured: {str(e)}')
      return Result.failure({
          "message": f'An unexpected error occured: {str(e)}'
      })

  def listUsers(self, filters):
    per_page = filters['per_page']
    page = filters['page']
    sort_by = 'id'

    try:
      with get_session() as session:
        skip = (page - 1) * per_page
        users = session.query(User).order_by(
            sort_by).limit(per_page).offset(skip).all()
        user_list = [{**map_user_data(user)} for user in users]
        self.logger.info(f'Retrieved users successfully')
        return Result.success({
            "message": "users retrieved successfully",
            "data": user_list
        })
    except Exception as e:
      self.logger.error(f"Error fetching user: {repr(e)}")
      return Result.failure({
          "error": "An error occurred while fetching user. Please try again later."
      })

  def delete(self, user_id):
    try:
      with get_session() as session:
        user = session.query(User).filter_by(id=user_id).one()
        session.delete(user)
        session.commit()
        self.logger.info(f'User deleted successfully: {user_id}')
        return Result.success({
            "message": "User deleted successfully",
        })
    except NoResultFound:
      self.logger.error(f'User with id {user_id} does not exist')
      return Result.failure({
          "message": "User not found",
          "status": 404
      })
    except Exception as e:
      self.logger.error(f'An unexpected error occured: {str(e)}')
      return Result.failure({
          "message": f'An unexpected error occured: {str(e)}'
      })
