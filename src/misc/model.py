from pydantic import BaseModel


class GetCodeForm(BaseModel):
    pw: str
    email: str
    redirect_url: str
    client_id: str
    status: str


class GetTokenForm(BaseModel):
    client_id: str
    client_pw: str
    code: str
    status: str
