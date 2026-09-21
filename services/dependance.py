from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jwt import decode_token
from typing import Annotated
from db.database import db_dependency
from schemas.auth import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(db:db_dependency,token: str = Depends(oauth2_scheme))-> User:
    playload= decode_token(token)
    if playload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )
    user_id = playload.get("sub")
    user_curent= db.query(User).filter(User.id == user_id).first()
    if not user_curent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable"
        )
    return user_curent





curent_dependancy = Annotated[int,Depends(get_current_user)]