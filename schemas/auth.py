from db.database import Base
from sqlalchemy import Column , String , Integer  , DateTime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column 


class CreateUser(Base):
        __tablename__="User"
        id:Mapped[int] = mapped_column(autoincrement=True , index=True , primary_key=True)
        name:Mapped[int]=mapped_column()
        prenom:Mapped[int]=mapped_column()
        email:Mapped[str] = mapped_column()
        password:Mapped[str]= mapped_column()
        createdAt:Mapped[DateTime]= Column(DateTime , default=DateTime.now())


class ConexionsValide(Base):
        email:Mapped[str] = mapped_column()
        password:Mapped[str]= mapped_column()
        
























