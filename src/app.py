from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

import re
import jwt
import datetime

from misc import HTMLGetter, Config, LoginForm

app = FastAPI()

email_regex = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
pw_regex = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

# 로그인 시에 API 서버와 연동해서 로그인 수행 후 토큰 발급하는 엔드포인트
@app.post('/login')
async def login(body : LoginForm):
    # 값 받아오기
    email : str= body.email
    pw : str= body.pw
    
    if email_regex.match(email) == None or pw_regex.match(pw) == None:
        raise HTTPException(status_code=400, detail="Bad Request")

    # API 연동
    try:
        data : dict() = await HTMLGetter(Config.API_SERVER).set_data(email = email, pw = pw).get_json()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="API Server Error")

    # data = {"pw" : pw, "email" : email} # API 서버 있을시에 해당 부분 주석 필요
    data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=600) # 10분의 기한
    encoded_data = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHEM) # 토큰화
    redirect_url = body.redirect_url# 리다이렉트 url 지정

    # return body setting
    # 307코드로 리다이렉트
    return RedirectResponse(f"{redirect_url}?code={encoded_data}", status_code=302)


# 테스트용 엔드포인트
# @app.get('/rb') 
# async def redirect_url(code : str):
#     return code