from ..models.user import User
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
        return None
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user.password_hash = password_hash
    db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
