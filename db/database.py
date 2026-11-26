import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from loguru import logger
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

URL = os.getenv("SQLALCHEMY_DATABASE_URL")
if URL:
    URL = URL.strip().strip('"').strip("'")

# Si la variable manque, on laisse l'API démarrer (health check) et on log un avertissement.
# Les routes qui utilisent la base lèveront une erreur explicite si elles sont appelées.
engine = None
if not URL:
    logger.warning(
        "SQLALCHEMY_DATABASE_URL n'est pas défini : l'API démarre sans base de données."
    )
else:
    # Neon fournit souvent une URL "postgresql://...?sslmode=require&channel_binding=require".
    # Le moteur est asynchrone : on force le driver asyncpg et on normalise les paramètres SSL.
    _db_url = make_url(URL).set(drivername="postgresql+asyncpg")
    _query = dict(_db_url.query)
    _query.pop("sslmode", None)
    _query.pop("channel_binding", None)
    _query["ssl"] = "require"
    engine = create_async_engine(_db_url.set(query=_query))

# DEF ENGINE / SESSION

async_session = async_sessionmaker(engine, expire_on_commit=False) if engine else None


class Base(DeclarativeBase):
    pass


# DEPENDENCY


async def get_db():
    if async_session is None:
        raise RuntimeError(
            "Base de données non configurée : SQLALCHEMY_DATABASE_URL est manquant."
        )
    db = async_session()
    try:
        yield db
    finally:
        await db.close()


db_dependency = Annotated[AsyncSession, Depends(get_db)]


async def init_db():
    if engine is None:
        logger.warning("init_db ignoré : aucune base de données configurée.")
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
