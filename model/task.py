from datetime import datetime

from db.database import Base
from model.user import User

from sqlalchemy import DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class CreateTask(Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        autoincrement=True,
        index=True,
        primary_key=True
    )

    title: Mapped[str] = mapped_column()

    description: Mapped[str] = mapped_column()

    priority: Mapped[str] = mapped_column()

    completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    userId: Mapped[int] = mapped_column(
        ForeignKey("User.id")
    )

    createdAt: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )