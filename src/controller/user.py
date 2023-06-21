from src.service.user.index import UserService

class UserController:
  def __init__(self, user_service: UserService):
    self.user_service = user_service
    pass
  
  def get(self):
    users = self.user_service.get()
    return users

  def create(self, user_data):
    return {'status': 'success', 'message': 'User created'}

  def listUsers(self, user_id):
    user = self.user_service.listUsers(user_id)
    return {'user': user}