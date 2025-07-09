from ..models.task_share import TaskShare
from ..models.task import Task
from ..models.user import User
from ..extensions import db

def share_task(task_id, user_email, permission='view'):
    user = User.query.filter_by(email=user_email).first()
    if not user:
        return {"message": "Usuário não encontrado."}, 404

    # Verifica se a tarefa existe
    task = Task.query.get(task_id)
    if not task:
        return {"message": "Tarefa não encontrada."}, 404

    # Verifica se já foi compartilhada
    existing = TaskShare.query.filter_by(task_id=task_id, user_id=user.id).first()
    if existing:
        return {"message": "Tarefa já compartilhada com este usuário."}, 400

    shared = TaskShare(task_id=task_id, user_id=user.id, permission=permission)
    db.session.add(shared)
    db.session.commit()

    return {"message": "Tarefa compartilhada com sucesso."}, 200

def get_task_shares(task_id):
    shares = TaskShare.query.filter_by(task_id=task_id).all()
    return [share.to_dict() for share in shares]

def remove_task_share(task_id, user_id):
    share = TaskShare.query.filter_by(task_id=task_id, user_id=user_id).first()
    if not share:
        return {"message": "Compartilhamento não encontrado."}, 404
    db.session.delete(share)
    db.session.commit()
    return {"message": "Compartilhamento removido com sucesso."}, 200
