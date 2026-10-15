from pydantic import BaseModel, EmailStr, Field
class RegisterRequest(BaseModel):
    username: str=Field(min_length=3,max_length=50)
    email: EmailStr
    password: str=Field(min_length=10,max_length=128)
    nombre: str=Field(min_length=2,max_length=100)
    apellido_paterno: str=Field(min_length=2,max_length=100)
    telefono: str|None=None
class Token(BaseModel): access_token: str; token_type: str="bearer"
class UserOut(BaseModel):
    id:int; username:str; email:EmailStr; role:str
