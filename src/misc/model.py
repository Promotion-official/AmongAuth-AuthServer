from pydantic import BaseModel


class GetCodeForm(BaseModel):
    pw: str
    email: str
    redirect_url: str
    client_id: str
    state: str


class GetTokenForm(BaseModel):
    client_id: str
    client_pw: str
    code: str
