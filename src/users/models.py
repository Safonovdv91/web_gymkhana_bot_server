from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, ForeignKey, false
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

from ..sport_classes.models import user_sport_class_associated_table


if TYPE_CHECKING:
    from ..roles.models import Role
    from ..sport_classes.models import SportClass


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # hashed_password: Mapped[str] = mapped_column(nullable=False)
    ggp_percent_begin: Mapped[int] = mapped_column(
        default=100,
    )
    ggp_percent_end: Mapped[int] = mapped_column(default=150)
    sub_ggp_percent: Mapped[bool] = mapped_column(default=False)
    sub_offline: Mapped[bool] = mapped_column(default=False)
    sub_ggp: Mapped[bool] = mapped_column(default=False)
    sub_world_record: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, server_default=false()
    )
    telegram_id: Mapped[Optional[int]]
    login: Mapped[Optional[str]]
    # email: Mapped[Optional[str]] = mapped_column(unique=True)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    # is_active: Mapped[bool] = mapped_column(
    #     Boolean,
    #     default=True,
    # )
    # is_superuser: Mapped[bool] = mapped_column(
    #     Boolean, default=False, nullable=False, server_default=false()
    # )
    # is_verified: Mapped[bool] = mapped_column(
    #     Boolean, default=False, nullable=False, server_default=false()
    # )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=1)
    role: Mapped["Role"] = relationship(back_populates="users")
    ggp_sub_classes: Mapped[List["SportClass"]] = relationship(
        secondary=user_sport_class_associated_table, back_populates="users"
    )

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (
            f" email: {self.email} "
            f"registered_at: {self.registered_at} "
            f"telegram_id: {self.telegram_id}"
        )
