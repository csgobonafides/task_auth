from fastapi import FastAPI, Request
from src.models._jwt import User, registed, authentifick, get_user_from_token, get_user_from_refresh_token
from src.models.parsers import data_films
from src.models.bl_lst import bl_list, open_list, exit_list
import asyncio

app = FastAPI()


@app.post('/register')
async def register(user: User):
    return registed(user.username, user.password)

@app.post('/auth')
async def auth(user: User):
    return authentifick(user.username, user.password)

@app.post('/data_film/{name_film}')
async def data_film(name_film, request: Request):
    print(request.headers.get('authorization'))
    if request.headers.get('authorization'):
        result = get_user_from_token(request.headers.get('authorization')[7:])
        print(result)
        if result == True:
            return await data_films(name_film)
        if result == 'Error ExpiredSignatureError':
            if request.headers.get('refresh'):
                check_refresh = get_user_from_refresh_token(request.headers.get('refresh'))
                if check_refresh != 'Error ExpiredSignatureError' and check_refresh != 'Error InvalidTokenError':
                    return check_refresh, await data_films(name_film)
        else:
            return result
    else:
        return {'message': 'Error'}

if __name__ == '__main__':
    import uvicorn
    try:
        open_list()
        uvicorn.run(app, host='127.0.0.1')
    finally:
        exit_list()