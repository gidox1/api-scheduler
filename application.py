import os
from flask import Flask

host=os.getenv('DATABASE_HOST')
user=os.getenv('DATABASE_USER') 
password=os.getenv('DATABASE_PASSWORD')
database=os.getenv('DATABASE_NAME')
authKey = os.getenv('AUTH_KEY')

app = Flask(__name__)

connection_string = f'mysql+pymysql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = authKey
