from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    email: str
    name: str
