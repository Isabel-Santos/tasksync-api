import os
from dotenv import load_dotenv
from datetime import timedelta
from pathlib import Path

load_dotenv()
#load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent.parent / '.env')
# print(f"🔐 JWT_SECRET_KEY carregado: {os.getenv('JWT_SECRET_KEY')}")
print("🔐 JWT_SECRET_KEY:", os.getenv("JWT_SECRET_KEY"))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "jwt_secret")
    # Configuração do JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret')  # Garantindo fallback se a variável de ambiente não estiver configurada
    #JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # Expiração do token em segundos (1 hora por padrão)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 10)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 604800)))  # 7 dias
    JWT_TOKEN_LOCATION = ['headers']
    
    # URL do banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_NAME = os.getenv('DATABASE_NAME')

    # MongoDB URI
    MONGO_URI = os.getenv("MONGO_URI")

    # Configuração do Google OAuth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
    
    # Cache (se necessário)
    CACHE_TYPE = os.getenv("CACHE_TYPE", "simple")
    CACHE_REDIS_URL = os.getenv("CACHE_REDIS_URL")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))

    # Configuração do Flask-Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ['true', '1']
    # MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ['true', '1']
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')