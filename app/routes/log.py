from flask import Blueprint, jsonify
from ..services.log_service import get_logs
from flask_cors import CORS

bp = Blueprint('log', __name__, url_prefix = '/logs')

@bp.route('/', methods = ['GET'])
def list_logs():
    logs = get_logs()
    return jsonify([{'id': log.id, 'action': log.action, 'timestamp': log.timestamp} for log in logs]), 200
