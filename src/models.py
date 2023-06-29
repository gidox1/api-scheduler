from flask_migrate import Migrate
from db import get_db
from application import app
from sqlalchemy import UniqueConstraint
from src.common import UserStatus, Role
import bcrypt

db = get_db()

"""
  User Model

  Args:
    db: DB model insitance
"""
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  phone_number = db.Column(db.String(15), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  role = db.Column(db.Enum(Role), nullable=False, default=Role.CUSTOMER)
  status = db.Column(
      db.Enum(UserStatus),
      nullable=False,
      default=UserStatus.ACTIVE)
  __table_args__ = (UniqueConstraint('email', name='uq_user_email'),)


"""
  Organization Model

  Args:
    db: DB model insitance
"""
class Organization(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), nullable=False, unique=True)
  country = db.Column(db.String(50), nullable=False)
  city = db.Column(db.String(50), nullable=True)
  address = db.Column(db.String(50), nullable=False)
  owner_id = db.Column(db.Integer, db.ForeignKey(User.id), unique=True)
  owner = db.relationship(User, backref='organization', uselist=False)


def loadModels():
  migrate = Migrate(app, db)
  User()
  Organization()


"""
  Model utils
"""
def verify_password(password, hashed_password):
  return bcrypt.checkpw(
      password.encode('utf-8'),
      hashed_password.encode('utf-8'))
