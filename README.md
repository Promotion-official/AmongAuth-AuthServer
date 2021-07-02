# Auth Server

## 기술스택
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)

## 실행방법

1. `Repository`를 `clone` 합니다.
```sh
git clone https://github.com/Promotion-official/AmongAuth-AuthServer.git
```

2. `requirement.txt`를 이용하여 필요한 `package`를 다운받습니다.
```sh
pip install -r requirements.txt
```

3. [환경변수를 입력해줍니다.](#환경-변수)

4. 다음 명령어를 통해 프로그램을 실행시킵니다.
```sh
python src/main.py -R -P 5225
# -R은 저장시 자동 실행 옵션이며, -P는 프로그램을 동작시킬 포트 번호이다. 공백시에 환경변수에 입력된 값으로 실행됩니다.
```

5. 다음으로 요청을 보내, 서버가 잘 작동하는지 확인을 한다.

## API 명세서

### POST /login
- request
```json
{
    "email" : "qudwls185@naver.com",
    "pw" : "1234",
    "redirect_url" : "http://0.0.0.0:4242/rb"
}
```

- 302 Found, 200 Succes
```sh
GET /rb?code=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdyI6IjEyMzQiLCJlbWFpbCI6InF1ZHdsczE4NUBuYXZlci5jb20ifQ.L-zOOPQwhgQHAubM0vc9eIy58LK3Gu4gC08IrAX0YDA
```

- 400 Bad Request
```json
{
    "detail": "Bad Request"
}
```

- 500 Intenal Server Error
```json
{
    "detail": "API Server Error"
}
```
