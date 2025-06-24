from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token

def generate_token(user_id):
    return create_access_token(identity=user_id)

@jwt_required()
def current_user_id():
    return get_jwt_identity()



