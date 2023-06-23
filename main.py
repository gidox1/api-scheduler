import configparser
import os
from dotenv import load_dotenv
from src.routes.user import user_routes
from application import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.model.user import user_model
from flask_jwt_extended import JWTManager

# Set up logging configuration
import logging
logging.basicConfig(
  filename='record.log', 
  level=logging.DEBUG, 
  format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s'
)

load_dotenv()
config = configparser.ConfigParser()
config._interpolation_depth = 15  # Increase interpolation depth limit

config.read('config.ini')
port = int(os.getenv('PORT', 5000))

## Register routes
app.register_blueprint(user_routes)

jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

user_model()

if __name__ == "__main__":
  app.run(host="localhost", port=port, debug=True)
