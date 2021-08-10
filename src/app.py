from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse

import re
import jwt
import datetime

from misc import HTMLGetter, Config, GetTokenForm, GetCodeForm

app = FastAPI()

email_regex = re.compile("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
pw_regex = re.compile("^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")

# 로그인 시에 API 서버와 연동해서 로그인 수행 후 토큰 발급하는 엔드포인트
@app.post("/get_code")
async def get_code(body: GetCodeForm):
    # 값 받아오기
    email: str = body.email
    pw: str = body.pw

    if email_regex.match(email) == None or pw_regex.match(pw) == None:
        raise HTTPException(status_code=400, detail="Bad Request")

    # API 연동
    try:
        data: dict() = (
            await HTMLGetter(Config.API_SERVER).get_json(email=email, pw=pw)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="API Server Error")

    # TODO DB 연동하여, 각 이메일과 client_id 쌍을 만들어, 액세스토큰 중복 체크

    # data = {"pw" : pw, "email" : email} # API 서버 있을시에 해당 부분 주석 필요
    data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=600
    )  # 10분의 기한
    data["client_id"] = body.client_id  # 클라이언트 id 지정

    encoded_data = jwt.encode(
        data, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHEM
    )  # 토큰화
    # endregion


    # TODO code의 방식을 redis로 옮길 필요 다분
    state = f"&state={body.state}"if body.state else ""
    redirect_url = f"{body.redirect_url}?code={encoded_data}{state}"  # 리다이렉트 url 지정
    
    # 302코드로 리다이렉트
    return RedirectResponse(redirect_url, status_code=302)


@app.post("/get_token")
async def get_token(body: GetTokenForm):
    # TODO client_id와 client_pw 체크 필요
    # TODO 추후 code 방식을 redis로 옮길 필요 있음
    try:
        jwt_data: str = jwt.verify(
            body.code, key=Config.JWT_SECRET, algorithms=Config.JWT_SECRET
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Unauthorized")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return jwt.encode(
        {"email": jwt_data.email, "client_id": jwt_data.client_id},
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHEM,
    )


# TODO client_pw 재발급 생성해야됨

# 테스트용 엔드포인트
# @app.get('/rb')
# async def redirect_url(code : str):
#     return code
