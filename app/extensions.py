from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_mail import Mail
import os

db = SQLAlchemy()
mongo_db_name = os.getenv('MONGO_DB_NAME', 'tasksync_db').strip()
print(f"🧪 Nome do MongoDB após strip: '{mongo_db_name}'")
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
mongo_db = client[os.getenv('MONGO_DB_NAME', 'tasksync_db')]
jwt = JWTManager()
cache = Cache()
oauth = OAuth()
mail = Mail()