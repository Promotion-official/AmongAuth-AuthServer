from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

import re
import jwt
import datetime

from misc import HTMLGetter, Config, GetTokenForm, GetCodeForm, CodeController

app = FastAPI()

app.add_middleware(DBSessionMiddleware(db_url=Config.DB_URL))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"]
)

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

    data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(
        seconds=600
    )  # 10분의 기한
    client_id = body.client_id
    data["client_id"] = client_id  # 클라이언트 id 지정

    code = jwt.encode(
        data, key=Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHEM
    )
    CodeController.delete(client_id=client_id, email=email)
    CodeController.add_code(client_id=client_id, email=email, code = code)


    # TODO code의 방식을 redis로 옮길 필요 다분
    state = f"&state={body.state}"if body.state else ""
    redirect_url = f"{body.redirect_url}?code={code}{state}"  # 리다이렉트 url 지정
    
    # 302코드로 리다이렉트
    return RedirectResponse(redirect_url, status_code=302)


@app.post("/get_token")
async def get_token(body: GetTokenForm):
    # TODO client_id와 client_pw 체크 필요
    # TODO 추후 code 방식을 redis로 옮길 필요 있음
    code = CodeController.get(code=body.code)
    
    token = jwt.encode(
        {"email": code.email, "client_id": code.client_id},
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHEM,
    )

    try:
        data = {"header" : {"Authorization" : Config.API_SERVER_KEY}, "body" : {"target_token" : token}}
        await HTMLGetter(f"{Config.API_SERVER}token/add-auth-token").get_json(data)

    except Exception as e :
        print(e)
        raise HTTPException(status_code=500, detail="API Server Error")

    return token


# TODO client_pw 재발급 생성해야됨

# 테스트용 엔드포인트
# @app.get('/rb')
# async def redirect_url(code : str):
#     return code
