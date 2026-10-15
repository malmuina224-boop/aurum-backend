from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.models.entities import User
from app.core.config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/token")
def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    payload=decode_token(token)
    if not payload or not payload.get("sub"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token invalido",headers={"WWW-Authenticate":"Bearer"})
    user=db.get(User,int(payload["sub"]))
    if not user or not user.Activo: raise HTTPException(status_code=401,detail="Usuario inactivo o inexistente")
    return user
