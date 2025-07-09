# from flask import Blueprint, request, jsonify, url_for, current_app
# # from werkzeug.security import check_password_hash, generate_password_hash
# from flask_jwt_extended import create_access_token, create_refresh_token ,jwt_required, get_jwt_identity, verify_jwt_in_request
# from .. import db, oauth, limiter, mail
# from flask_mail import Message
# from ..models.user import User
# from ..services.auth_service import authenticate_user, register_user, request_password_reset, reset_user_password
# from flask_cors import cross_origin

# bp = Blueprint('auth', __name__, url_prefix='/auth')

# # Rota de login refatorada
# @bp.route('/login', methods=['POST'])
# # @cross_origin(origins=["https://localhost:3000"], supports_credentials=True)
# # @cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
# @limiter.limit("5 per minute")
# def login():
#     try:
#         data = request.get_json()
#         print(f"Login tentativa para email: {data.get('email')}")
#         # 1. Verificação de dados obrigatórios
#         if not data or 'email' not in data or 'password' not in data:
#             return jsonify({'message': 'Email e senha são obrigatórios!'}), 400
#         # 2. Autenticar usuário via service
#         response, status_code = authenticate_user(data['email'], data['password'])
#         print(f"authenticate_user retornou status {status_code} e resposta {response}")
#         if status_code == 200:
#             user_id = response['user_id']
#             # 3. Gerar access token (curto prazo) e refresh token (longo prazo)
#             access_token = create_access_token(identity=str(user_id))
#             refresh_token = create_refresh_token(identity=str(user_id))
#             # 4. Retornar tokens e dados básicos do usuário
#             rep = ({
#                 'message': 'Login realizado com sucesso!',
#                 'access_token': access_token,
#                 'refresh_token': refresh_token,
#                 'user': {
#                     'id': user_id,
#                     'username': response['username'],
#                     'email': response['email']
#                 }
#             })
#             print(rep)
#             return jsonify(rep), 200
#         # 5. Caso falhe na autenticação
#         return jsonify(response), status_code
#     except Exception as e:
#         print(f"[LOGIN ERROR] {e}")
#         return jsonify({'message': 'Erro interno no servidor, tente novamente.'}), 500

# # Rota de cadastro de usuário
# @bp.route('/signup', methods=['POST'])
# def signup():
#     try:
#         data = request.get_json()
#         if not data or 'email' not in data or 'password' not in data or 'username' not in data:
#             return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400
#         response, status_code = register_user(data)
#         return jsonify(response), status_code
#     except Exception:
#         return jsonify({'message': 'Erro interno no servidor, tente novamente.'}), 500

# # Rota de refresh token
# @bp.route('/refresh', methods=['POST'])
# @jwt_required(refresh=True)
# def refresh():
#     current_user = get_jwt_identity()
#     new_access_token = create_access_token(identity=current_user)
#     return jsonify({'access_token': new_access_token}), 200

# # Rota de validadação do token
# @bp.route('/debug', methods=['GET'])
# def debug_token():
#     try:
#         verify_jwt_in_request()
#         user_id = get_jwt_identity()
#         return jsonify({"valid": True, "user_id": user_id})
#     except Exception as e:
#         return jsonify({"valid": False, "error": str(e)})

# # Rota de redefinição de senha
# @bp.route('/forgot-password', methods=['POST'])
# @limiter.limit("3 per minute")
# def forgot_password():
#     data = request.get_json()
#     email = data.get('email')
#     if not email:
#         return jsonify({"message": "E-mail é obrigatório"}), 400
#     response, status = request_password_reset(email)
#     return jsonify(response), status

# # Rota de preenchimento de senha nova
# @bp.route("/reset-password", methods=["POST"])
# @limiter.limit("5 per minute")
# def reset_password():
#     data = request.get_json()
#     token = request.args.get("token")
#     new_password = data.get("new_password")
#     if not token or not new_password:
#         return jsonify({"message": "Token e nova senha são obrigatórios."}), 400
#     return reset_user_password(token, new_password)

# # Rota protegida para testar a autenticação com JWT
# @bp.route('/protected', methods=['GET'])
# @jwt_required()  # Esta rota exige um token válido
# def protected():
#     current_user_id = get_jwt_identity()  # Recupera a identidade do usuário do token
#     return jsonify(logged_in_as=current_user_id), 200

# # Rota para login com Google usando OAuth
# @bp.route('/login/google')
# def login_with_google():
#     return oauth.google.authorize_redirect(url_for('auth.google_callback', _external=True))

# # Rota de callback do Google após login com OAuth
# @bp.route('/login/google/callback')
# def google_callback():
#     token = oauth.google.authorize_access_token()
#     user_info = oauth.google.parse_id_token(token)
#     # Verifica se o usuário existe no banco de dados
#     user = User.query.filter_by(email=user_info['email']).first()
#     if not user:
#         user = User(username=user_info['name'], email=user_info['email'])
#         db.session.add(user)
#         db.session.commit()
#     # Gera o token JWT para o usuário autenticado via Google
#     jwt_token = create_access_token(identity=str(user.id))  # Convertendo o ID para string
#     return jsonify({'token': jwt_token})


# # # Rota para testar o token JWT (opcional, para depuração)
# # @bp.route('/login/test', methods=['GET'])
# # def test_token():
# #     token = request.headers.get('Authorization')
# #     if token:
# #         try:
# #             decoded_token = decode_token(token.split()[1], allow_expired=True)  # Extrai o token do cabeçalho Authorization
# #             print("Token decodificado:", decoded_token)  # Log do token decodificado
# #             return jsonify({"message": "Token válido", "decoded_token": decoded_token}), 200
# #         except Exception as e:
# #             print("Erro ao decodificar o token:", e)
# #             return jsonify({"message": "Token inválido!"}), 401
# #     else:
# #         return jsonify({"message": "Token não fornecido!"}), 400

from flask import Blueprint, request, jsonify, url_for, current_app
from flask_jwt_extended import create_access_token, create_refresh_token ,jwt_required, get_jwt_identity, verify_jwt_in_request
from .. import db, oauth, limiter, mail
from flask_mail import Message
from ..models.user import User
from ..services.auth_service import authenticate_user, register_user, request_password_reset, reset_user_password
from flask_cors import cross_origin
import random
import string

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'message': 'Email e senha são obrigatórios!'}), 400
        response, status_code = authenticate_user(data['email'], data['password'])
        if status_code != 200:
            return jsonify(response), status_code
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({'message': 'Usuário não encontrado.'}), 404
        # Gerar código 2FA
        code = ''.join(random.choices(string.digits, k=6))
        user.twofa_code = code
        db.session.commit()
        # Enviar código por e-mail
        msg = Message('Seu código 2FA - TaskSync', sender='noreply@tasksync.com', recipients=[user.email])
        msg.body = f"Olá, {user.username}!\n\nSeu código de verificação é: {code}\n\nDigite este código para concluir seu login."
        mail.send(msg)
        return jsonify({"message": "Código de verificação enviado para o e-mail."}), 200
    except Exception as e:
        print(f"[LOGIN ERROR] {e}")
        return jsonify({'message': 'Erro interno no servidor, tente novamente.'}), 500

@bp.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    try:
        data = request.get_json()
        email = data.get("email")
        code = data.get("code")
        if not email or not code:
            return jsonify({"message": "Email e código são obrigatórios."}), 400
        user = User.query.filter_by(email=email).first()
        if not user or not user.twofa_code:
            return jsonify({"message": "Verificação inválida."}), 401
        if user.twofa_code != code:
            return jsonify({"message": "Código incorreto."}), 401
        # Limpa o código 2FA
        user.twofa_code = None
        db.session.commit()
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        return jsonify({
            'message': 'Login realizado com sucesso!',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200

    except Exception as e:
        print(f"[2FA ERROR] {e}")
        return jsonify({'message': 'Erro interno no servidor, tente novamente.'}), 500

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

@bp.route('/forgot-password', methods=['POST'])
@limiter.limit("3 per minute")
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"message": "E-mail é obrigatório"}), 400
    response, status = request_password_reset(email)
    return jsonify(response), status

@bp.route("/reset-password", methods=["POST"])
@limiter.limit("5 per minute")
def reset_password():
    data = request.get_json()
    token = request.args.get("token")
    new_password = data.get("new_password")
    if not token or not new_password:
        return jsonify({"message": "Token e nova senha são obrigatórios."}), 400
    return reset_user_password(token, new_password)

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200

@bp.route('/login/google')
def login_with_google():
    return oauth.google.authorize_redirect(url_for('auth.google_callback', _external=True))

@bp.route('/login/google/callback')
def google_callback():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.parse_id_token(token)
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(username=user_info['name'], email=user_info['email'])
        db.session.add(user)
        db.session.commit()
    jwt_token = create_access_token(identity=str(user.id))
    return jsonify({'token': jwt_token})
