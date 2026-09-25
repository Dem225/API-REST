from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jwt import decode_token
from typing import Annotated

from db.database import db_dependency
from model.user import User

from sqlalchemy import select


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/connexion")


async def get_current_user(
    db: db_dependency,
    token: str = Depends(oauth2_scheme)
) -> User:

    playload = decode_token(token)

    if playload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )

    user_id = int(playload.get("sub"))

    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    
    user_curent = result.scalar_one_or_none()

    if not user_curent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur introuvable"
        )

    return user_curent


curent_user_dependancy = Annotated[
    User,
    Depends(get_current_user)
]