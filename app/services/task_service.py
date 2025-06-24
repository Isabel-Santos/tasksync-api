from flask import jsonify
from ..models.task import Task
from ..extensions import db, cache
from flask_jwt_extended import get_jwt_identity
from ..services.log_service import create_log
import json


ALLOWED_STATUSES = {"A fazer", "Em andamento", "Concluída"}


def validate_task_data(title, description, status):
    if not isinstance(title, str) or not isinstance(status, str):
        raise ValueError("Título e status devem ser do tipo string!")
    if len(title) < 5:
        raise ValueError("O título deve ter pelo menos 5 caracteres!")
    if not description or len(description) < 10:
        raise ValueError("A descrição deve ter pelo menos 10 caracteres!")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Status inválido. Use um dos valores permitidos: {', '.join(ALLOWED_STATUSES)}.")
    return True


def create_task(data, user_id):
    try:
        status = data.get('status', 'A fazer')
        validate_task_data(data['title'], data.get('description', ''), status)
        new_task = Task(title=data['title'], description=data.get('description', ''), status=data.get('status', 'A fazer'), user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        create_log(f"Tarefa criada: {new_task.title}", user_id)
        cache.delete(f"tasks:{user_id}")
        return jsonify({'message': 'Tarefa criada com sucesso', 'task': new_task.to_dict()}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    except Exception:
        return jsonify({'message': 'Erro interno ao criar tarefa'}), 500


def get_tasks(user_id):
    cached_tasks = cache.get(f"tasks:{user_id}")
    if cached_tasks:
        return jsonify(json.loads(cached_tasks))
    tasks = Task.query.filter_by(user_id=user_id).all()
    tasks_list = [{"id": task.id, "title": task.title, "description": task.description, "status": task.status} for task in tasks]
    cache.set(f"tasks:{user_id}", json.dumps(tasks_list), timeout=300)  # ✅ CORRETO
    return jsonify(tasks_list)


def get_all_tasks(user_id):
    cache_key = f"tasks:{user_id}"
    cached_tasks = cache.get(cache_key)
    if cached_tasks:
        return json.loads(cached_tasks)
    tasks = Task.query.filter_by(user_id=user_id).all()
    tasks_data = [{'id': t.id, 'title': t.title, 'status': t.status} for t in tasks]
    cache.set(cache_key, json.dumps(tasks_data), timeout=300)  # Cache por 5 minutos
    return tasks_data


def update_task(task_id, data, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'message': 'Tarefa não encontrada'}), 404
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao salvar as alterações'})
    create_log(f"Tarefa atualizada: {task.title}", user_id)
    cache.delete(f"tasks:{user_id}")
    cache.delete(f"task:{user_id}:{task_id}")
    return jsonify({'message': 'Tarefa atualizada'})


def delete_task(task_id, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({'message': 'Tarefa não encontrada'}), 404
    db.session.delete(task)
    db.session.commit()
    create_log(f"Tarefa excluída: {task.title}", user_id)
    cache.delete(f"tasks:{user_id}")
    return jsonify({'message': 'Tarefa removida'})


def get_task_by_id(user_id, task_id):
    cache_key = f"task:{user_id}:{task_id}"
    cached_task = cache.get(cache_key)
    if cached_task:
        return json.loads(cached_task)
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return None
    task_data = task.to_dict()
    cache.set(cache_key, json.dumps(task_data), timeout=300)
    return task_data


def get_tasks_by_title(title):
    return Task.query.filter(Task.title.ilike(f"%{title}%")).all()


def get_tasks_by_status(status):
    return Task.query.filter_by(status=status).all()


def get_tasks_by_criteria(task_id=None, title=None, status=None):
    query = Task.query
    if task_id:
        query = query.filter(Task.id == task_id)
    if title:
        query = query.filter(Task.title.ilike(f'%{title}%'))
    if status:
        query = query.filter(Task.status == status)
    return query.all()


def get_task_from_cache(task_id, user_id):
    cache_key = f"task:{user_id}:{task_id}"
    task = cache.get(cache_key)
    if task:
        return task
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task:
        task_data = {"id": task.id, "title": task.title, "description": task.description, "user_id": task.user_id}
        cache.set(cache_key, task_data)
        return task_data
    return None
