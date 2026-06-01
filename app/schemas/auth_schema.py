from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    username: str
    password: str


class RegisterUserResponse(BaseModel):
    message: str
    access_token: str


class LoginUserRequest(BaseModel):
    username: str
    password: str


class LoginUserResponse(BaseModel):
    message: str
    access_token: str
