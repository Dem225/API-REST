from fastapi import APIRouter, Depends

from schemas.auth import Conexions, UserCreate
from services.auth import AuthService
from typing import Annotated
from db.database import db_dependency
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(
    prefix="/auth",
    tags=["AUTH"]
)

# model.Base.metadata.create_all(bind=engine)



@auth_router.post("/inscriptions")
async def Inscriptions(body: UserCreate,db: db_dependency):
    service = AuthService(db)

    return await service.inscription(body)


@auth_router.post("/connexion")
async def Connexion(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    service = AuthService(db)
    body = Conexions(email=form_data.username, password=form_data.password)

    return await service.connexion(body) 