from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token, decode_token
from datetime import timedelta

def generate_token(user_id):
    return create_access_token(identity=user_id)

@jwt_required()
def current_user_id():
    return get_jwt_identity()

def generate_reset_password_token(user_id):
    return create_access_token(identity=str(user_id), expires_delta=timedelta(minutes=15), additional_claims={"reset_password":True})

def decode_reset_password_token(token):
    decoded = decode_token(token)
    if not decoded.get("reset_password"):
        raise ValueError("Token inválido para definição de senha.")
    return decoded