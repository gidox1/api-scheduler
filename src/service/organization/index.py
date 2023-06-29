import logging

from src.common import Result, handleError
from db import get_session
from src.models import Organization
from src.mapper import convert_to_dict, map_org_data
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload


class OrganizationService:
  def __init__(self, logger: logging.Logger):
    self.logger = logger
    pass


  def create(self, data):
    dbSession = get_session(True)
    session = None
    with dbSession as session:
      session.begin()
      try:
        org = Organization(**data)
        exists = session.query(Organization).filter_by(
            owner_id=data['owner_id']).first()
        if exists:
          return Result.failure({
              "message": "Only one organization is permitted to be created per user",
          })
        session.add(org)
        session.flush()
      except BaseException:
        session.rollback()
        message = "Failed to create organization"
        return handleError(
            ValueError("Failed to create organization"),
            message,
            self.logger)
      else:
        session.commit()
        self.logger.info(
            f"organization with name '{data['name']}' created successfully")
        return Result.success({
            "message": "organization created successfully",
            "data": convert_to_dict(org)
        })


  def update(self, data, user_id, org_id):
    self.logger.info(f"Updating organization data for og with id {org_id}")
    with get_session() as session:
      try:
        org = session.query(Organization).filter_by(
            owner_id=user_id, id=org_id
        ).options(
            joinedload(Organization.owner)
        ).one()
        allowed_keys = ['name', 'country',
                        'city', 'address', 'org_url']
        updated_fields = {key: value for key,
                          value in data.items() if key in allowed_keys}

        # set updated fields
        for key, value in updated_fields.items():
          setattr(org, key, value)

        session.commit()
        msg = "organization updated successfully"
        self.logger.info(msg)
        return Result.success({
            "message": msg,
            "data": convert_to_dict(org)
        })
      except NoResultFound:
        self.logger.error(
            f'Organization does not exist for user with id {user_id} and org_id of {org_id}')
        return Result.failure({
            "message": "Organization not found",
            "status": 404
        })
      except Exception as e:
        message = "Failed to update organization"
        return handleError(e, message, self.logger)


  def delete(self, org_id, user_id):
    self.logger.info(
        f"started process of deleting organization with id {org_id} by user {user_id}")
    session = get_session()
    try:
      org = session.query(Organization).filter_by(
          owner_id=user_id, id=org_id
      ).one()
      session.delete(org)
      session.commit()
      msg = f"Deleted organization with id {org_id} successfully"
      self.logger.info(msg)
      return Result.success({
          "message": msg,
          "org_id": org_id
      })
    except NoResultFound:
      self.logger.error(
          f'Organization does not exist for user with id {user_id} and org_id of {org_id}')
      return Result.failure({
          "message": "Organization not found",
          "status": 404
      })
    except Exception as e:
      message = "Failed to fetch organization"
      return handleError(e, message, self.logger)


  def get(self, org_id, user_id):
    self.logger.info(f"Fetching data for organization with id {org_id}")
    with get_session() as session:
      try:
        org = session.query(Organization).filter_by(
            owner_id=user_id, id=org_id
        ).options(
            joinedload(Organization.owner)
        ).one()

        self.logger.info(
            f'Retrieved organization successfully: {org_id}')
        return Result.success({
            "message": "organization retrieved successfully",
            "data": map_org_data(org)
        })
      except NoResultFound:
        self.logger.error(
            f'Organization does not exist for user with id {user_id} and org_id of {org_id}')
        return Result.failure({
            "message": "Organization not found",
            "status": 404
        })
      except Exception as e:
        message = "Failed to fetch organization"
        return handleError(e, message, self.logger)


  def listOrgs(self):
    pass
