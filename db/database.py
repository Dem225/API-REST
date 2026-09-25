
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker , Session, DeclarativeBase
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

import os
from dotenv import load_dotenv
load_dotenv()
URL=os.getenv("SQLALCHEMY_DATABASE_URL_URI")

# DEF ENGINE

engine = create_async_engine(URL)


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