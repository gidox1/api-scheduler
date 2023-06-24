from db import get_db
from src.common import UserStatus, Role
from flask_migrate import Migrate
from application import app
from sqlalchemy import UniqueConstraint
import bcrypt

db = get_db()


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  phone_number = db.Column(db.String(15))
  password = db.Column(db.String(100), nullable=False)
  role = db.Column(db.Enum(Role), nullable=False, default=Role.CUSTOMER)
  status = db.Column(
      db.Enum(UserStatus),
      nullable=False,
      default=UserStatus.ACTIVE)
  __table_args__ = (UniqueConstraint('email', name='uq_user_email'),)


def user_model():
  migrate = Migrate(app, db)
  return User()


def verify_password(password, hashed_password):
  return bcrypt.checkpw(
      password.encode('utf-8'),
      hashed_password.encode('utf-8'))
