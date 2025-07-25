from flask import Flask, jsonify, app, request
from flask_cors import CORS
from flask_login import LoginManager
from .extensions import db, jwt, oauth, cache, mail, limiter
from .config import Config
from .routes import auth, user, task, log
from .routes.task_share import bp as task_share
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import os

load_dotenv()

def create_database_if_not_exists(app):
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    conn = psycopg2.connect(host=db_host, port=db_port, user=db_user, password=db_password)
    conn.autocommit = True

    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
            if not cursor.fetchone():
                print(f"Banco de dados {db_name} não encontrado. Criando banco...")
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
                print(f"Banco de dados {db_name} criado com sucesso.")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar criar o banco de dados: {e}")
    finally:
        conn.close()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app,
        origins=["https://localhost:3000"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "X-User-ID"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    
    print("✅✅✅ O SERVIDOR ESTÁ RODANDO COM A CONFIGURAÇÃO CORS CORRETA! ✅✅✅")
    
    print(f"🔐 DEBUG - JWT_SECRET_KEY na verificação: {os.getenv('JWT_SECRET_KEY')}")
    print(f"🧪 DEBUG - Config carregada: {Config.JWT_SECRET_KEY}")

    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    oauth.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    @jwt.unauthorized_loader
    def unauthorized_response(callback):
        return jsonify({"message": "Token não fornecido ou inválido!"}), 401

    @jwt.invalid_token_loader
    def invalid_token_response(error):
        return jsonify({"message": "Token inválido!"}), 401

    @jwt.expired_token_loader
    def expired_token_response(error):
        return jsonify({"message": "Token expirado!"}), 401
    
    # @jwt.invalid_token_loader
    # def invalid_token_callback(error):
    #     print(f"Invalid token error: {error}")
    #     return jsonify({"message": "Token inválido!"}), 401
    
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models.user import User
        return User.query.get(int(user_id))

    with app.app_context():
        create_database_if_not_exists(app)
        db.create_all()

    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(task)
    app.register_blueprint(log)
    app.register_blueprint(task_share)


    # @app.after_request
    # def apply_cors_headers(response):
    #     origin = request.headers.get('Origin')
    #     allowed_origin = "https://localhost:3000"

    #     if origin == "https://localhost:3000":
    #         response.headers["Access-Control-Allow-Origin"] = origin
    #         response.headers["Access-Control-Allow-Credentials"] = "true"
    #         response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization,X-User-ID"
    #         response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"

    #     print(f"🔍 Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin')}")
    #     print(f"🔍 Access-Control-Allow-Credentials: {response.headers.get('Access-Control-Allow-Credentials')}")
    #     return response

    return app