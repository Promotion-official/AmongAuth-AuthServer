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

### POST /get_code

- request

```json
{
  "pw": "str",
  "email": "email",
  "redirect_url": "redirect_url",
  "client_id": "client_id",
  "state": "str"
}
```

`email`, `pw`는 사용자가 사용할 이메일과 비밀번호를 뜻한다.  
`redirect_url`은 사용자가 로그인 시, 리다이렉트 될 URL을 뜻한다.  
`client_id`는 해당 정보가 들어갈 클라이언트의 고유 id를 뜻한다.  
`state`의 경우, 값이 변질된 사항이 있는지 체크하는 방식이며, `optional`의 특성을 지닌다.

> `state`의 경우, response 값이랑 이어집니다.

- response

```
GET redirect_url?code={encoded_data}&state=state
redirect_url=redirect_url
```

여기서 `state`의 경우 `request`에서 온 값을 기준으로 한다.

### POST /get_token

- request

```json
{
  "client_id": "str",
  "client_pw": "str",
  "code": "str"
}
```

`client_id`의 경우 해당 클라이언트를 뜻하는 고유 id값을 뜻합니다.
`client_pw`의 경우 해당 클라이언트의 `password`를 뜻합니다.
`code`의 경우, `POST /get_code`에서 얻게 된 `code`를 뜻합니다.

- response

```
smaple jwt value
```

### POST /get_new_client_pw

#### TODO 언젠가 작성하겠지, 해당 코드도 없느디...
