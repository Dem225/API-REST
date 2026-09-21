from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class User(Base):

    __tablename__ = "User"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        primary_key=True,
        index=True
    )

    nom: Mapped[str] = mapped_column()

    prenom: Mapped[str] = mapped_column()

    email: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )

    password: Mapped[str] = mapped_column()

    createdAt: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )