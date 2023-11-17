from sqlalchemy import text
import asyncio
from src.database import engine

print("Добавляем стандартные роли")

async def add_roles():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("INSERT INTO roles VALUES(1, 'Super_User','Can change role all users/admins, "
                                    "delete or create')"))
            await conn.execute(text("INSERT INTO roles VALUES(2, 'Admin','Administrator can del users, and change user's "
                                    "settings')"))
            await conn.execute(text("INSERT INTO roles VALUES(3, 'User','Can only change himself settings')"))
            await conn.execute(text("INSERT INTO roles VALUES(4, 'Guest','Unknown person, can nothing')"))
        except Exception as e:
            print("<----Добавление пошло не по плану!---->")
            print(f"ERROR: {e}")


asyncio.run(add_roles())
