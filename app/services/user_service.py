from flask import jsonify
from ..models.user import User
from ..utils.validators import is_valid_email, is_valid_username, is_strong_password
from .. import db, app
import bcrypt

def create_user(username, email, password):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return user

def get_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def update_user(user_id, username=None, email=None, password=None):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Usuário não encontrado."}), 404
    if username:
        if not is_valid_username(username):
            return jsonify({"message": "Nome de usuário inválido. Deve ter pelo menos 3 caracteres alfanuméricos."})
        user.username = username
    if email:
        if not is_valid_email(email):
            return jsonify({"message": "Email inválido."}), 400
        user.email = email
    if password:
        if not is_strong_password(password):
            return jsonify({"message":"A senha deve ter no mínimo 8 caracteres."}), 400
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user.password_hash = password_hash
    db.session.commit()
    return jsonify({"message": "Usuário atualizado com sucesso.", "user": {"id": user.id, "username": user.username, "email": user.email}}), 200

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
