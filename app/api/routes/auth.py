from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.models.entities import Role, User, Client
from app.schemas.auth import RegisterRequest, Token, UserOut
from app.api.deps import get_current_user
router=APIRouter()
@router.post("/register",response_model=UserOut,status_code=201)
def register(data:RegisterRequest,db:Session=Depends(get_db)):
    if db.scalar(select(User).where((User.Correo==data.email)|(User.NombreUsuario==data.username))): raise HTTPException(409,"Correo o usuario ya registrado")
    role=db.scalar(select(Role).where(Role.NombreRol=="Cliente",Role.Activo==True))
    if not role: raise HTTPException(500,"Rol Cliente no configurado")
    user=User(RolID=role.RolID,NombreUsuario=data.username,Correo=data.email,PasswordHash=hash_password(data.password),Activo=True,CorreoVerificado=False,FechaCreacion=datetime.now())
    db.add(user); db.flush()
    db.add(Client(UsuarioID=user.UsuarioID,Nombre=data.nombre,ApellidoPaterno=data.apellido_paterno,ApellidoMaterno=None,Telefono=data.telefono,Activo=True))
    db.commit(); db.refresh(user)
    return UserOut(id=user.UsuarioID,username=user.NombreUsuario,email=user.Correo,role=role.NombreRol)
@router.post("/token",response_model=Token)
def login(form:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    user=db.scalar(select(User).where((User.Correo==form.username)|(User.NombreUsuario==form.username)))
    if not user or not verify_password(form.password,user.PasswordHash): raise HTTPException(401,"Credenciales incorrectas",headers={"WWW-Authenticate":"Bearer"})
    return Token(access_token=create_access_token(str(user.UsuarioID),user.role.NombreRol))
@router.get("/me",response_model=UserOut)
def me(user:User=Depends(get_current_user)): return UserOut(id=user.UsuarioID,username=user.NombreUsuario,email=user.Correo,role=user.role.NombreRol)
