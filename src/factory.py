from typing import Dict
from src.service.user.index import UserService
from src.controller.user import UserController
from pymysql import Connection
from db import connection
from flask import current_app
from application import app
import logging


class ServiceFactory:

  def __init__(self) -> None:
    pass

  @staticmethod
  def get_version() -> Dict[str, str]:
    return {
        "version": "1.0.0",
        "licence": "MIT"
    }

  @staticmethod
  def get_logger() -> logging.Logger:
    with app.app_context():
      logger = current_app.logger
      return logger

  @staticmethod
  def get_user_controller() -> UserController:
    logger = ServiceFactory.get_logger()
    service = UserService(logger)
    return UserController(service)
  
  @staticmethod
  def get_user_service() -> UserService:
    logger = ServiceFactory.get_logger()
    return UserService(logger)

  @staticmethod
  def get_connection() -> Connection:
    return connection()
