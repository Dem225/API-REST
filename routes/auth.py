
from fastapi import APIRouter 
from services.auth import AuthServiceInscrip
from schemas.auth import CreateUser
from schemas.auth import ConexionsValide
from starlette import status
from services.auth  import AuthServiceConnexion
from db import listes_utlisateur


auth_router=APIRouter(prefix="/auth" , tags=["AUTH"])


@auth_router.post("/inscriptions")
def Inscriptions(body:CreateUser):
    serice =AuthServiceInscrip()
    return serice.inscription(body)



@auth_router.post("/connexion")
def Connexion(body:ConexionsValide):
    services=AuthServiceConnexion()
    return services.Connexions(body)



@auth_router.post("/deconnexion")
def Deconnexion():
    return "page de déconnexion"

@auth_router.get("/AllUser" , status_code=status.HTTP_200_OK)
def All_User():
    return listes_utlisateur


