import jwt
from datetime import timedelta, datetime, timezone
from pydantic import BaseModel
from src.models.bl_lst import bl_list

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
                print(payload.get('exp'))
                return True
    except jwt.ExpiredSignatureError:
        return 'Error ExpiredSignatureError'
    except jwt.InvalidTokenError:
        return 'Error InvalidTokenError'

def get_user_from_refresh_token(refresh: str):
    try:
        payload = jwt.decode(refresh, SECRET_KEY, algorithms=ALGORITM)
        if refresh not in bl_list.get('refresh'):
            for user in USER_DATA:
                if user.get('login') == payload.get('login'):
                    bl_list.get('refresh').append(refresh)
                    token = create_jwt_token({'login': user.get('login'), 'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=1)})
                    refresh_token = create_jwt_token({'login': user.get('login'), 'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=10)})
                    return {"Новый assens token": token, 'Новый refresh token': refresh_token}
        return {'message': 'Not authentication'}
    except jwt.ExpiredSignatureError:
        return 'Error ExpiredSignatureError'
    except jwt.InvalidTokenError:
        return 'Error InvalidTokenError'


def authentifick(login, psw):
    for user in USER_DATA:
        if user.get('login') == login and user.get('password') == psw:
            '''Костыль'''
            # token = create_jwt_token({'login': f'{login}', 'exp': datetime.now() - timedelta(days=0, hours=4, minutes=59)})
            '''Красиво'''
            token = create_jwt_token({'login': f'{login}', 'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=1)})
            refresh_token = create_jwt_token({'login': f'{login}', 'exp': datetime.now(tz=timezone.utc) + timedelta(minutes=10)})
            return {'message': 'Вы успешно авторизовались',
                    'assens': token,
                    'refresh': refresh_token}
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