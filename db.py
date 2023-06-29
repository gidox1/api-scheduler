import os
import pymysql
from pymysql import Connection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as dbSession
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from application import app
from flask import current_app

host=os.getenv('DATABASE_HOST')
user=os.getenv('DATABASE_USER') 
password=os.getenv('DATABASE_PASSWORD')
database=os.getenv('DATABASE_NAME')
port=os.getenv('DATABASE_PORT', 3310)

def connection() -> Connection:
  try:
    conn = pymysql.connect(
      host,
      user,
      password,
      database,
      port,
      cursorclass=pymysql.cursors.DictCursor
    )
    print("successfully connected to the database")
    return conn
  except Exception as e:
    print("failed to connect to database", e)

def get_session(trx=False):
  pymysql_connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'
  engine = create_engine(pymysql_connection_string)
  Session = sessionmaker(bind=engine)
  if trx:
    return dbSession(engine)
  return Session()

def get_connection_string() -> str:
  return f'mysql+pymysql://{user}:{password}@{host}/{database}'

def get_db():
  with app.app_context():
    return SQLAlchemy(current_app)
