import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
mongo_db_name = os.getenv('MONGO_DB_NAME', 'tasksync_db').strip()
print(f"🧪 Nome do MongoDB após strip: '{mongo_db_name}'")
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
mongo_db = client[os.getenv('MONGO_DB_NAME', 'tasksync_db')]
jwt = JWTManager()
cache = Cache()
oauth = OAuth()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per day", "25 per hour"]
)