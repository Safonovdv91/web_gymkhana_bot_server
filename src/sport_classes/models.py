from typing import TYPE_CHECKING, List

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


if TYPE_CHECKING:
    from ..users.models import User

user_sport_class_associated_table = Table(
    "ggp_subclasses_lists",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("sport_classes_id", ForeignKey("sport_classes.id"), nullable=False),
    UniqueConstraint(
        "user_id", "sport_classes_id", name="idx_unique_user_class"
    ),
)


class SportClass(Base):
    __tablename__ = "sport_classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    sport_class: Mapped[str] = mapped_column(String(2), unique=True)
    description: Mapped[str | None]
    users: Mapped[List["User"]] = relationship(
        secondary=user_sport_class_associated_table,
        back_populates="ggp_sub_classes",
    )
