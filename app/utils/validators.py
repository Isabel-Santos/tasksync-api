import re
ALLOWED_STATUSES = {"A fazer", "Em andamento", "Concluída"}

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_username(username):
    return len(username) >= 3 and username.isalnum()

def is_strong_password(password):
    return len(password) >= 8

def is_valid_task_data(title, description, status):
    if not isinstance(title, str) or not isinstance(status, str):
        raise ValueError("Título e status devem ser do tipo string!")
    if len(title) < 5:
        raise ValueError("O título deve ter pelo menos 5 caracteres!")
    if not description or len(description) < 10:
        raise ValueError("A descrição deve ter pelo menos 10 caracteres!")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Status inválido. Use um dos valores permitidos: {', '.join(ALLOWED_STATUSES)}.")
    return True