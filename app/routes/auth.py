from flask import Blueprint, request, jsonify, url_for, current_app
# from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token ,jwt_required, get_jwt_identity, verify_jwt_in_request
from .. import db, oauth
from ..models.user import User
from ..services.auth_service import authenticate_user, register_user
from flask_cors import cross_origin

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Rota de login (autenticação com JWT) FUNCIONAL
# @bp.route('/login', methods=['POST'])
# @cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
# def login():
#     try:
#         data = request.get_json()
#         if not data or 'email' not in data or 'password' not in data:
#             return jsonify({'message': 'Email e senha são obrigatórios!'}), 400
#         response, status_code = authenticate_user(data['email'], data['password'])
#         if status_code == 200:
#             response['token'] = create_access_token(identity=int(response['user_id']))
#         return jsonify(response), status_code
#     except Exception:
#         return jsonify({'message': 'Erro interno no servidor, tente novamente.'}), 500

# Rota de login refatorada
@bp.route('/login', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def login():
    try:
        data = request.get_json()
        # 1. Verificação de dados obrigatórios
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Email e senha são obrigatórios!'}), 400
        # 2. Autenticar usuário via service
        response, status_code = authenticate_user(data['email'], data['password'])
        if status_code == 200:
            user_id = response['user_id']
            # 3. Gerar access token (curto prazo) e refresh token (longo prazo)
            access_token = create_access_token(identity=str(user_id))
            refresh_token = create_refresh_token(identity=str(user_id))
            # 4. Retornar tokens e dados básicos do usuário
            return jsonify({
                'message': 'Login realizado com sucesso!',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user_id,
                    'username': response['username'],
                    'email': response['email']
                }
            }), 200
        # 5. Caso falhe na autenticação
        return jsonify(response), status_code
    except Exception as e:
        print(f"[LOGIN ERROR] {e}")
        return jsonify({'message': 'Erro interno no servidor, tente novamente.'}), 500

# Rota de cadastro de usuário
@bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data or 'username' not in data:
            return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400
        response, status_code = register_user(data)
        return jsonify(response), status_code
    except Exception:
        return jsonify({'message': 'Erro interno no servidor, tente novamente.'}), 500

# Rota de refresh token
@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': new_access_token}), 200


@bp.route('/debug', methods=['GET'])
def debug_token():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return jsonify({"valid": True, "user_id": user_id})
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)})


# # Rota para testar o token JWT (opcional, para depuração)
# @bp.route('/login/test', methods=['GET'])
# def test_token():
#     token = request.headers.get('Authorization')
#     if token:
#         try:
#             decoded_token = decode_token(token.split()[1], allow_expired=True)  # Extrai o token do cabeçalho Authorization
#             print("Token decodificado:", decoded_token)  # Log do token decodificado
#             return jsonify({"message": "Token válido", "decoded_token": decoded_token}), 200
#         except Exception as e:
#             print("Erro ao decodificar o token:", e)
#             return jsonify({"message": "Token inválido!"}), 401
#     else:
#         return jsonify({"message": "Token não fornecido!"}), 400

# Rota protegida para testar a autenticação com JWT
@bp.route('/protected', methods=['GET'])
@jwt_required()  # Esta rota exige um token válido
def protected():
    current_user_id = get_jwt_identity()  # Recupera a identidade do usuário do token
    return jsonify(logged_in_as=current_user_id), 200

# Rota para login com Google usando OAuth
@bp.route('/login/google')
def login_with_google():
    return oauth.google.authorize_redirect(url_for('auth.google_callback', _external=True))

# Rota de callback do Google após login com OAuth
@bp.route('/login/google/callback')
def google_callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    
    # Verifica se o usuário existe no banco de dados
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(username=user_info['name'], email=user_info['email'])
        db.session.add(user)
        db.session.commit()
    
    # Gera o token JWT para o usuário autenticado via Google
    jwt_token = create_access_token(identity=str(user.id))  # Convertendo o ID para string
    return jsonify({'token': jwt_token})