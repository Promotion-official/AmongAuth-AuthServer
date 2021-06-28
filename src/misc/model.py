from pydantic import BaseModel

class LoginForm(BaseModel):
    pw : str
    email : str
    redirect_url : str
    token : str = ""