from flask import Blueprint, request, jsonify
from ..services.user_service import create_user, get_users, get_user_by_id, update_user, delete_user
from flask_cors import CORS

bp = Blueprint('user', __name__, url_prefix = '/users')

@bp.route('/', methods=['GET'])
def list_users():
    users = get_users()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users]), 200

@bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Todos os campos são obrigatórios!'}), 400
    user = create_user(data['username'], data['email'], data['password'])
    return jsonify({'message': 'Usuário criado com sucesso!', 'user_id': user.id}), 201

    
@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify({"id": user.id, "username": user.username, "email": user.email}), 200
    return jsonify({'error': 'Usuário não encontrado!'}), 404

# Atualizar um usuário
@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    user = update_user(user_id, username, email, password)
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 200
    return jsonify({'error': 'Usuário não encontrado!'}), 404

# Remover um usuário
@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    if delete_user(user_id):
        return jsonify({'message': 'Usuário removido com sucesso!'}), 200
    return jsonify({'error': 'Usuário não encontrado!'}), 404