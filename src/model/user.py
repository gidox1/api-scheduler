from db import get_db
from src.common import UserStatus, Role
from flask_migrate import Migrate
from application import app

db = get_db()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    password = db.Column(db.String(100))
    role = db.Column(db.Enum(Role))
    status = db.Column(db.Enum(UserStatus))

def user_model():
    migrate = Migrate(app, db)
    return User()