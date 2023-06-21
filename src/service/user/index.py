import logging

class UserService:
  def __init__(self, logger: logging.Logger):
    self.logger = logger
    pass
  
  def get(self):
    self.logger.info('fetching users')
    return {'users': "users here"}

  def create(self):
    return {'status': 'success', 'message': 'User created'}

  def listUsers(self):
    return {'user': 'user'}