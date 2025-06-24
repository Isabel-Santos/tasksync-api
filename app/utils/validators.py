import re

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_username(username):
    return len(username) >= 3 and username.isalnum()

def is_strong_password(password):
    return len(password) >= 8