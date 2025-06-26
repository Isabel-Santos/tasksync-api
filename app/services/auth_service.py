from flask import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from ..utils.validators import is_valid_email, is_valid_username, is_strong_password, is_unique_email
from ..utils.jwt_helper import generate_token, generate_reset_password_token, decode_reset_password_token
from ..models.user import User
from ..extensions import db
import bcrypt


def verify_and_upgrade_password(user, password):
    try:
        stored_hash = user.password_hash
        if stored_hash.startswith("$2b$"):  # Bcrypt padrão
            return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        elif stored_hash.startswith("pbkdf2:sha256"):
            if check_password_hash(stored_hash, password):
                # Atualiza a senha para bcrypt
                new_bcrypt_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user.password_hash = new_bcrypt_hash.decode('utf-8')
                db.session.commit()
                return True
        return False
    except Exception as e:
        print(f"[ERRO verify_and_upgrade_password] {e}")
        return False


def authenticate_user(email, password):
    try:
        user = User.query.filter_by(email=email).first()
        if not user or not verify_and_upgrade_password(user, password):
    # check werkzeug    if not user or not check_password_hash(user.password_hash, password):
            return {'message': 'Credenciais inválidas'}, 401
        return {'user_id': user.id, 'username': user.username, 'email': user.email}, 200
    except Exception as e:
        print(f"[AUTH ERROR] {e}")
        return {'message': 'Erro interno ao autenticar usuário.'}, 500


def register_user(data):
    try:
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        # Validações de entrada
        if not all([email, username, password]):
            return {'message': 'Todos os campos são obrigatórios!'}, 400
        if not is_valid_username(username):
            return {'message': 'Nome de usuário deve conter ao menos 3 caracteres alfanuméricos.'}, 400
        if not is_valid_email(email):
            return {'message': 'Email inválido!'}, 400    
        if not is_strong_password(password):
            return {'message': 'A senha deve conter no mínimo 8 caracteres, com pelo menos uma letra maiúscula, uma minúscula, um número e um caractere especial.'}, 400
        # Verificação de existência de email
        if not is_unique_email(email):
            return {'message': 'Email já cadastrado!'}, 409
        # Criação de usuário
        bcrypt_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        # hashed_password = generate_password_hash(data['password'], method="pbkdf2:sha256")
        new_user = User(email=data['email'], username=data['username'], password_hash=bcrypt_hash)
        db.session.add(new_user)
        db.session.commit()
        jwt_token = generate_token(new_user.id)
        return {'message': 'Usuário cadastrado com sucesso!', 'token': jwt_token}, 201
    except Exception as e:
        print(f"[REGISTER ERROR] {e}")
        return {'message': 'Erro interno ao cadastrar usuário.'}, 500


def request_password_reset(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"message": "Se o email existir, enviaremos instruções"}, 200
    token = generate_reset_password_token(user.id)
    reset_link = f"http://localhost:5000/auth/reset-password?token={token}"
    print(f"🔗 Link de redefinição (simulado): {reset_link}")
    return {"message": "Se o e-mail existir, enviaremos instruções."}, 200


def reset_user_password(token, new_password):
    try:
        decoded_token = decode_reset_password_token(token)
        user_id = decoded_token.get("sub")
        user = User.query.get(user_id)
        if not user:
            return {"message": "Usuário não encontrado."}, 404
        # Atualiza a senha com bcrypt
        new_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user.password_hash = new_hash
        db.session.commit()
        return {"message": "Senha redefinida com sucesso!"}, 200
    except Exception as e:
        return {"message": f"Erro ao redefinir a senha: {str(e)}"}, 400