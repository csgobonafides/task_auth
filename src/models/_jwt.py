import jwt
from datetime import timedelta, datetime
from pydantic import BaseModel

SECRET_KEY = 'secretkey'
ALGORITM = 'HS256'

USER_DATA = [
    {"login": "bona", "password": "admin"}
]

class User(BaseModel):
    username: str
    password: str

def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITM)

def get_user_from_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITM)
        for user in USER_DATA:
            if user.get('login') == payload.get('login'):
                return True
    except jwt.ExpiredSignatureError:
        return 'Error ExpiredSignatureError'
    except jwt.InvalidTokenError:
        return 'Error InvalidTokenError'

def authentifick(login, psw):
    for user in USER_DATA:
        if user.get('login') == login and user.get('password') == psw:
            token = create_jwt_token({'login': f'{login}', 'exp': datetime.now() + timedelta(days=0, minutes=1)})
            return {'Вы успешно авторизовались, вот ваш токен': token}
        elif user.get('login') == login and user.get('password') != psw:
            return {'message': 'Вы указали неверный пороль.'}
    return {'message': 'Пользователь с такими данными не найден.'}

def name_chek(login):
    for user in USER_DATA:
        if user.get('login') == login:
            return False
    return True

def registed(login, psw):
    if not name_chek(login):
        return {'message': 'Пользователь с таким логином уже зарегистрирован.'}
    else:
        USER_DATA.append({'username': f'{login}', 'password': f'{psw}'})
        return {'message': 'Вы успешно зарегистрированы.'}