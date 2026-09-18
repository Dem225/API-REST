
from db.database import Base
from schemas.auth import CreateUser
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column 

from sqlalchemy.dialects.postgresql import ARRAY   



class CreateTask(Base):
        __tablename__="tasks"
        id:Mapped[int] = mapped_column(autoincrement=True , index=True , primary_key=True)
        title:Mapped[str] = mapped_column()
        description:Mapped[str] = mapped_column()
        priorty:Mapped[str] = mapped_column()
        completd:Mapped[str]=mapped_column(Boolean)
        userId:Mapped[int] = mapped_column(ForeignKey("User.id"))
        createdAt= mapped_column(DateTime)