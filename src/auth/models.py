from datetime import datetime
from typing import Optional

from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, ForeignKey, Integer,
                        String, Table, MetaData)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

metadata = MetaData()

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    ggp_percent_begin: Mapped[int] = mapped_column(default=100, )
    ggp_percent_end: Mapped[int] = mapped_column(default=150)
    sub_ggp_percent: Mapped[int] = mapped_column(default=False)
    sub_offline: Mapped[bool] = mapped_column(default=False)
    sub_ggp: Mapped[bool] = mapped_column(default=False)
    sub_world_record: Mapped[bool] = mapped_column(default=False)
    telegram_id: Mapped[Optional[int]]
    login: Mapped[Optional[str]]
    email: Mapped[Optional[str]] = mapped_column(unique=True)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, login: str, password: str, email:str
    ) -> User:
        new_user = User(
            hashed_password=password,
            login=login,
            email=email
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
