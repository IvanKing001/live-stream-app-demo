from functools import wraps
from flask import request, Response

# 🔑 Задаємо логін і пароль
USERNAME = "admin"
PASSWORD = "secret123"

def check_auth(username, password):
    """Перевіряє логін і пароль"""
    return username == USERNAME and password == PASSWORD

def authenticate():
    """Відповідь при невірних даних"""
    return Response(
        "Доступ заборонено", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    """Декоратор для захисту маршрутів"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
