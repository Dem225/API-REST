from fastapi import APIRouter

from schemas.auth import Conexions, UserCreate
from services.auth import AuthService
from db.database import db_dependency , Base , engine
import model

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
async def Connexion( body: Conexions,db: db_dependency):
    service = AuthService(db)

    return await service.connexion(body)