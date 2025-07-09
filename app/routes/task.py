from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.task_service import create_task, get_tasks, update_task, delete_task, get_task_by_id, get_all_tasks
from flask_cors import cross_origin

bp = Blueprint('task', __name__, url_prefix='/tasks')


@bp.route('/add', methods=['POST'])
@jwt_required()
def add_task():
    user_id = str(get_jwt_identity())
    if not isinstance(user_id, str):  # Garantindo que o user_id seja um número string
        return jsonify({'message': 'ID do usuário inválido no token'}), 400
    return create_task(request.get_json(), user_id)


@bp.route('/list', methods=['GET'], strict_slashes=False)
@jwt_required()
@cross_origin(origins="https://localhost:3000", supports_credentials=True)
def list_tasks():
    user_id = get_jwt_identity()
    if not isinstance(user_id, str):  # Garantindo que o user_id seja um número string
        return jsonify({'message': 'ID do usuário inválido no token'}), 400
    tasks = get_all_tasks(user_id)
    if not tasks:
        return jsonify({'message': 'Nenhuma tarefa encontrada'}), 404
    return jsonify(tasks), 200


@bp.route('/get/<int:task_id>', methods=['GET'])
@jwt_required()
@cross_origin(origins="https://localhost:3000", supports_credentials=True)
def get_task(task_id):
    user_id = get_jwt_identity()
    if not isinstance(user_id, str):  # Garantindo que o user_id seja um número inteiro
        return jsonify({'message': 'ID do usuário inválido no token'}), 400
    task = get_task_by_id(user_id, task_id)
    if not task:
        return jsonify({'message': 'Task não encontrada ou não pertencente ao usuário'}), 404
    return jsonify(task), 200


@bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
@cross_origin(origins="https://localhost:3000", supports_credentials=True)
def edit_task(task_id):
    user_id = get_jwt_identity()
    return update_task(task_id, request.get_json(), user_id)


@bp.route('/<int:task_id>/remove', methods=['DELETE'])
@jwt_required()
@cross_origin(origins="https://localhost:3000", supports_credentials=True)
def remove_task(task_id):
    user_id = get_jwt_identity()
    return delete_task(task_id, user_id)


# @bp.route('/<int:user_id>/<int:task_id>', methods=['GET'])
# @jwt_required()
# @cross_origin(origins="https://localhost:3000", supports_credentials=True, allow_headers=["Content-Type", "Authorization"])
# def get_task(user_id, task_id):
#     token_user_id = get_jwt_identity()  # Obtém o user_id do token JWT
#     print(f"User ID do token JWT: {token_user_id}")  # Adiciona log para verificar o user_id do token
#     print(f"User ID da URL: {user_id}")  # Adiciona log para verificar o user_id da URL

#     if user_id != token_user_id:
#         return jsonify({'message':'Acesso negado!'}), 403

#     task = get_task_by_id(task_id, user_id)
#     if not task or task:
#         return jsonify({'message': 'Tarefa não encontrada ou acesso negado!'}), 404

#     return jsonify(task), 200