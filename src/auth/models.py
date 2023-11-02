from datetime import datetime
from typing import Optional, List

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, MetaData, false, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


metadata = MetaData()


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    hashed_password: Mapped[str] = mapped_column(
        nullable=False
    )
    ggp_percent_begin: Mapped[int] = mapped_column(
        default=100,
    )
    ggp_percent_end: Mapped[int] = mapped_column(
        default=150
    )
    sub_ggp_percent: Mapped[bool] = mapped_column(
        default=False
    )
    sub_offline: Mapped[bool] = mapped_column(
        default=False
    )
    sub_ggp: Mapped[bool] = mapped_column(
        default=False
    )
    sub_world_record: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, server_default=false()
    )
    telegram_id: Mapped[Optional[int]]
    login: Mapped[Optional[str]]
    email: Mapped[Optional[str]] = mapped_column(
        unique=True
    )
    registered_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True,
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, server_default=false()
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, server_default=false()
    )

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=1)

    role: Mapped["Role"] = relationship(back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), unique=True)
    description: Mapped[str | None] = mapped_column()

    users: Mapped[List["User"]] = relationship(
        back_populates="role"
    )

class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, login: str, password: str, email: str) -> User:
        new_user = User(hashed_password=password, login=login, email=email)

        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
