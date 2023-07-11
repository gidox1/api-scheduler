from flask_migrate import Migrate
from db import get_db
from application import app
from sqlalchemy import UniqueConstraint
from src.common import UserStatus, Role
from datetime import datetime
import bcrypt

db = get_db()

"""
  User Model

  Args:
    db: DB model instance
"""


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  phone_number = db.Column(db.String(15), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  role = db.Column(db.Enum(Role), nullable=False, default=Role.CUSTOMER)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(
      db.DateTime,
      default=datetime.utcnow,
      onupdate=datetime.utcnow)
  status = db.Column(
      db.Enum(UserStatus),
      nullable=False,
      default=UserStatus.ACTIVE)
  __table_args__ = (UniqueConstraint('email', name='uq_user_email'),)
  organizations = db.relationship(
      'Organization',
      back_populates='owner',
      cascade='all, delete',
      passive_deletes=True,
      uselist=False)
  franchise_manager = db.relationship(
      'Franchise',
      back_populates='manager',
      cascade='all, delete',
      passive_deletes=True,
      uselist=False)


"""
  Organization Model

  Args:
    db: DB model instance
"""


class Organization(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), nullable=False, unique=True)
  country = db.Column(db.String(50), nullable=False)
  city = db.Column(db.String(50), nullable=True)
  address = db.Column(db.String(50), nullable=False)
  owner_id = db.Column(
      db.Integer,
      db.ForeignKey(
          User.id,
          ondelete="CASCADE"),
      unique=True)
  owner = db.relationship(User, back_populates='organizations', uselist=False)
  franchises = db.relationship(
      'Franchise',
      back_populates='franchise_organization',
      cascade='all, delete',
      passive_deletes=True)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  updated_at = db.Column(
      db.DateTime,
      default=datetime.utcnow,
      onupdate=datetime.utcnow)


"""
  Franchise Model

  Args:
    db: DB model instance
"""

class Franchise(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    country = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=True)
    manager_id = db.Column(
        db.Integer,
        db.ForeignKey(User.id, ondelete="CASCADE"),
        unique=True
    )
    organization_id = db.Column(
        db.Integer,
        db.ForeignKey(Organization.id, ondelete="CASCADE")
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    manager = db.relationship(User, back_populates='franchise_manager', uselist=False)
    franchise_organization = db.relationship(
        Organization,
        back_populates='franchises',
        uselist=False
    )


def loadModels():
  Migrate(app, db)
  User()
  Organization()


"""
  Model utils
"""


def verify_password(password, hashed_password):
  return bcrypt.checkpw(
      password.encode('utf-8'),
      hashed_password.encode('utf-8'))
