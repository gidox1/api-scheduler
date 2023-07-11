from typing import Dict
from src.service.user import UserService
from src.service.organization import OrganizationService
from src.service.franchise import FranchiseService
from src.controller.user import UserController
from src.controller.organization import OrganizationController
from src.controller.franchise import FranchiseController
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
    service = ServiceFactory.get_user_service()
    return UserController(service)

  @staticmethod
  def get_user_service() -> UserService:
    logger = ServiceFactory.get_logger()
    return UserService(logger)

  @staticmethod
  def get_connection() -> Connection:
    return connection()

  @staticmethod
  def get_org_service() -> OrganizationService:
    logger = ServiceFactory.get_logger()
    return OrganizationService(logger)

  @staticmethod
  def get_org_controller() -> OrganizationController:
    service = ServiceFactory.get_org_service()
    return OrganizationController(service)

  @staticmethod
  def get_franchise_service() -> FranchiseService:
    user_service = ServiceFactory.get_user_service()
    logger = ServiceFactory.get_logger()
    return FranchiseService(logger, user_service)

  @staticmethod
  def get_franchise_controller() -> FranchiseController:
    service = ServiceFactory.get_franchise_service()
    return FranchiseController(service)
