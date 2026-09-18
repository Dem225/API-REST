from schemas.auth import CreateUser
from fastapi import FastAPI, Query , Body,HTTPException
from schemas.auth import ConexionsValide
from schemas.auth_id import add_id
from db import listes_utlisateur

class AuthServiceInscrip:
    def inscription(self, user:CreateUser=Body):
        for users in listes_utlisateur :
            if users.email== user.email:
                raise HTTPException(status_code=409 , detail=" l'untilisateur que vous voulez ajouter existe deja")
        listes_utlisateur.append(add_id(user))
        return listes_utlisateur





class AuthServiceConnexion:
    def Connexions(self , user:ConexionsValide):
        for  users in listes_utlisateur:
            if users.email==user.email and users.password==user.password:
              return {"status" : True , "data" :user }
        raise HTTPException(status_code=401 , detail="mode de passe ou mail inconrecte")




