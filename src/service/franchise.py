import logging
from db import get_session
from sqlalchemy.exc import NoResultFound
from src.common import Result, handleError, extract
from src.models import User, Organization
from sqlalchemy.orm import joinedload, load_only
from src.mapper import convert_to_dict
from src.service.user import UserService
from src.models import Franchise


class FranchiseService:
  def __init__(self, logger: logging, user_service: UserService):
    self.logger = logger
    self.user_service = user_service
    pass

  def create(self, data):
    self.logger.info(f"started process of creating franchise with data {str(data)}")

    with get_session() as session:
        try:
            user_org = session.query(Organization).options(load_only('owner_id', 'id')).filter_by(
                owner_id=data['user_id']).one_or_none()

            if user_org is None:
                err_msg = 'organization does not exist'
                return handleError(ValueError(err_msg), err_msg, self.logger, 404)
            
            if user_org.id != data['org_id']:
                err_msg = 'organization does not belong to user'
                return handleError(ValueError(err_msg), err_msg, self.logger, 400)

            admin_id = data.get('manager_id')

            if admin_id:
                manager = session.query(User).filter_by(id=admin_id).one_or_none()
                if not manager:
                    err_msg = 'manager with the provided ID does not exist'
                    return handleError(ValueError(err_msg), err_msg, self.logger, 400)

            elif data.get('admin_details'):
                userCreationResult = self.user_service.create(data['admin_details'])
                if Result.isError(userCreationResult):
                    session.rollback()
                    err = "Invalid admin data"
                    return handleError(ValueError(err), err, self.logger)
                admin_id = userCreationResult.value['data']['id']

            franchise = Franchise(
                name=data['name'],
                country=data['country'],
                address=data['address'],
                city=data['city'],
                manager_id=admin_id,
                organization_id=data['org_id']
            )

            session.add(franchise)
            session.flush()
        except Exception as e:
            session.rollback()
            message = "Failed to create franchise"
            handleError(e, message, self.logger)
            raise e
        else:
            session.commit()
            self.logger.info(
                f"franchise with name '{data['name']}' created successfully")
            return Result.success({
                "message": "franchise created successfully",
                "data": convert_to_dict(franchise)
            })


  def update(self, data):
    pass

  def get(self, data):
    pass

  def listFranchise(self, data):
    pass
