from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), unique=True)
    description: Mapped[str | None] = mapped_column()

    users: Mapped[List["User"]] = relationship(back_populates="role")
