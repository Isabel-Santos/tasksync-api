import re

ALLOWED_STATUSES = {"A fazer", "Em andamento", "Concluída"}

def is_valid_email(email):
    if not isinstance(email, str):
        return False
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def is_valid_username(username):
    return isinstance(username, str) and len(username) >= 3 and username.isalnum()

def is_strong_password(password):
    if not isinstance(password, str) and len(password) >= 8:
        return False
    has_upper = re.search(r"[A-Z]", password)
    has_lower = re.search(r"[a-z]", password)
    has_digit = re.search(r"[0-9]", password)
    has_special = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)
    return all([has_upper, has_lower, has_digit, has_special])

def is_valid_task_data(title, description, status):
    if not isinstance(title, str) or not isinstance(status, str):
        raise ValueError("Título e status devem ser do tipo string.")
    if len(title.strip()) < 5:
        raise ValueError("O título deve ter pelo menos 5 caracteres.")
    if not isinstance(description, str) or len(description.strip()) < 10:
        raise ValueError("A descrição deve conter no mínimo 10 caracteres.")
    if status not in ALLOWED_STATUSES:
        raise ValueError(f"Status inválido. Use um dos valores permitidos: {', '.join(ALLOWED_STATUSES)}.")
    return True