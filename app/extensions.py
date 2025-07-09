from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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

# Função para limitar por IP ou ID do usuário (se logado)
def get_user_or_ip():
    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
    try:
        verify_jwt_in_request(optional=True)
        user = get_jwt_identity()
        if user:
            return f"user:{user}"
    except Exception:
        pass
    return get_remote_address()

limiter = Limiter(
    key_func=get_user_or_ip,
    default_limits=["200 per day", "50 per hour"]
)