from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


if TYPE_CHECKING:
    from ..users.models import User


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    description: Mapped[str | None] = mapped_column()

    users: Mapped[List["User"]] = relationship(back_populates="role")

    def __str__(self):
        return f"Role # {self.id} - [ {self.name} ]"
