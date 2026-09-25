from schemas.auth import Conexions, UserCreate
from model.user import User
from db.database import db_dependency

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import select
from passlib.context import CryptContext
from jwt import create_token


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class AuthService:

    def __init__(self, db: db_dependency):
        self.db = db

    async def inscription(self, Body_user: UserCreate):

        # Vérifier si l'utilisateur existe déjà
        result = await self.db.execute(select(User).where(User.email == Body_user.email))

        utilisateur_existe = result.scalar_one_or_none()

        if utilisateur_existe:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Utilisateur exists déjà !")

        # Hacher le mot de passe
        password_hash = pwd_context.hash(Body_user.password)

        # Créer le nouvel utilisateur
        new_user = User(
            nom=Body_user.nom,
            prenom=Body_user.prenom,
            email=Body_user.email,
            password=password_hash
        )

        self.db.add(new_user)

        await self.db.commit()
        await self.db.refresh(new_user)

        logger.info("Utilisateur créé avec succès")

        return new_user

    async def connexion(self, user: Conexions):
        # Rechercher l'utilisateur avec son email
        result = await self.db.execute(
            select(User).where(User.email == user.email)
        )
       
        User_db = result.scalar_one_or_none()
        print(User_db)
        # Vérifier l'utilisateur et le mot de passe
        if not User_db or not pwd_context.verify(
            user.password,
            User_db.password
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mot de passe ou email invalide !"
            )

        # Création du token
        access_token = create_token({"sub": str(User_db.id)})

        return { "access_token": access_token}