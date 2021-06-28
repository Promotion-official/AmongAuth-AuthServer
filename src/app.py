from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import jwt

from misc import HTMLGetter, Config, LoginForm

app = FastAPI()

@app.post('/login')
async def login(body : LoginForm):
    email = body.email
    pw = body.pw

    data = await HTMLGetter(Config.API_SERVER).set_data(email = email, pw = pw).get_json()
    data = {"pw" : pw, "email" : email}
    encoded_data = jwt.encode(data, Config.JWT_SECRET, algorithm=Config.JWT_ALGORITHEM)
    redirect_url = body.redirect_url

    # return body setting
    body.email = ""
    body.pw = ""

    body.token = encoded_data

    return RedirectResponse(redirect_url, headers={"Authorization" : encoded_data}, status_code=307)

