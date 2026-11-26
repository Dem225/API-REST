
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker , Session, DeclarativeBase
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

import os
from dotenv import load_dotenv
from sqlalchemy.engine import make_url
load_dotenv()
URL=os.getenv("SQLALCHEMY_DATABASE_URL")
if not URL:
    raise RuntimeError(
        "SQLALCHEMY_DATABASE_URL n'est pas défini : ajoute-le dans ton fichier .env "
        "(voir .env.example)."
    )

# Neon fournit souvent une URL "postgresql://...?sslmode=require&channel_binding=require".
# Le moteur est asynchrone : on force le driver asyncpg et on normalise les paramètres SSL.
_db_url = make_url(URL).set(drivername="postgresql+asyncpg")
_query = dict(_db_url.query)
_query.pop("sslmode", None)
_query.pop("channel_binding", None)
_query["ssl"] = "require"

# DEF ENGINE

engine = create_async_engine(_db_url.set(query=_query))


#DEF OF SESSION

async_session = async_sessionmaker(engine, expire_on_commit=False)

# DEF BASE AN OBJECT TO USER


class Base(DeclarativeBase):
    pass



#DEPENDENCY

async def get_db():
    db=async_session()
    try:
        yield db
    finally:
        await db.close()

#DEPENDANCY ANNOTATED


db_dependency = Annotated[AsyncSession, Depends(get_db)]


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)