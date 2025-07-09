from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.task_share_service import share_task, get_task_shares, remove_task_share

bp = Blueprint('task_share', __name__, url_prefix='/tasks')

@bp.route('/<int:task_id>/share', methods=['POST'])
@jwt_required()
def share(task_id):
    data = request.get_json()
    email = data.get('email')
    permission = data.get('permission', 'view')
    if not email:
        return jsonify({"message": "E-mail é obrigatório."}), 400
    return share_task(task_id, email, permission)

@bp.route('/<int:task_id>/shared', methods=['GET'])
@jwt_required()
def list_shared_users(task_id):
    shares = get_task_shares(task_id)
    return jsonify(shares), 200

@bp.route('/<int:task_id>/unshare/<int:user_id>', methods=['DELETE'])
@jwt_required()
def unshare(task_id, user_id):
    return remove_task_share(task_id, user_id)
