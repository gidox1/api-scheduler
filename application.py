import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

host=os.getenv('DATABASE_HOST')
user=os.getenv('DATABASE_USER') 
password=os.getenv('DATABASE_PASSWORD')
database=os.getenv('DATABASE_NAME')

app = Flask(__name__)

connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # or True
