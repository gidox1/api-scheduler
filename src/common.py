from enum import Enum

class UserStatus(Enum):
  ACTIVE = 'ACTIVE'
  INACTIVE = 'INACTIVE'
  
class Role(Enum):
  ADMIN = 'ADMIN'
  CUSTOMER = 'CUSTOMER'
  SUPER_ADMIN = 'SUPER_ADMIN'