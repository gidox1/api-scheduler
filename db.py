import os
import pymysql
from pymysql import Connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from application import app
from flask import current_app

host=os.getenv('DATABASE_HOST', '127.0.0.1')
user=os.getenv('DATABASE_USER', 'schUser') 
password=os.getenv('DATABASE_PASSWORD', 'schPass')
db=os.getenv('DATABASE_NAME', 'schDB')

def connection() -> Connection:
  try:
    conn = pymysql.connect(
      host='localhost',
      user='schUser',
      password='schPass',
      database='schDB',
      port=3310,
      cursorclass=pymysql.cursors.DictCursor
    )
    print("successfully connected to the database")
    return conn
  except Exception as e:
    print("failed to connect to database", e)

def get_session():
  pymysql_connection_string = f'mysql+pymysql://{user}:{password}@{host}/{db}'
  engine = create_engine(pymysql_connection_string)
  Session = sessionmaker(bind=engine)
  return Session()

def get_connection_string() -> str:
  return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_db():
  with app.app_context():
    return SQLAlchemy(current_app)
