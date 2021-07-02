from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

import jwt

from misc import HTMLGetter, Config, LoginForm

app = FastAPI()

# 로그인 시에 API 서버와 연동해서 로그인 수행 후 토큰 발급하는 엔드포인트
@app.post('/login')
async def login(body : LoginForm):
    # 값 받아오기
    email = body.email
    pw = body.pw

    if email == None or pw == None:
        HTTPException(status_code=400, detail="Bad Request")

    # API 연동
    try:
        data = await HTMLGetter(Config.API_SERVER).set_data(email = email, pw = pw).get_json()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="API Server Error")

    # data = {"pw" : pw, "email" : email} # API 서버 있을시에 해당 부분 주석 필요

    encoded_data = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHEM) # 토큰화
    redirect_url = body.redirect_url# 리다이렉트 url 지정

    # return body setting
    body.email = ""
    body.pw = ""
    body.token = encoded_data

    # 307코드로 리다이렉트
    return RedirectResponse(redirect_url, status_code=307)

