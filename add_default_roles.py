from sqlalchemy import text
import asyncio
from src.database import engine


async def add_roles():
    print("Добавляем стандартные роли и спортинвые классы")
    async with engine.begin() as conn:
        try:
            await conn.execute(
                text(
                    "INSERT INTO roles (name, description) VALUES('Super_User','Can change role all users/admins, "
                    "delete or create')"
                )
            )
            await conn.execute(
                text(
                    "INSERT INTO roles (name, description) VALUES('Admin','Administrator can del users, and change users "
                    "settings')"
                )
            )
            await conn.execute(
                text(
                    "INSERT INTO roles (name, description) VALUES('User','Can only change himself settings')"
                )
            )
            await conn.execute(
                text(
                    "INSERT INTO roles (name, description) VALUES('Guest','Unknown person, can nothing')"
                )
            )
            await conn.execute(
                text(
                    "INSERT INTO sport_classes (sport_class, description) VALUES('A','Best of the best')"
                )
            )
            await conn.execute(
                text(
                    "INSERT INTO sport_classes (sport_class, description) VALUES('B','Sport mans: 100-105 %')"
                )
            )
            await conn.execute(
                text(
                    "INSERT INTO sport_classes (sport_class, description) VALUES('C1','Sport mans: 105-110 %')"
                )
            )
            await conn.execute(
                text(
                    "INSERT INTO sport_classes (sport_class, description) VALUES('C2','Sport mans: 110-115 %')"
                )
            )
            await conn.execute(
                text(
                    "INSERT INTO sport_classes (sport_class, description) VALUES('C3','Sport mans: 115-120 %')"
                )
            )

        except Exception as e:
            print("<----Добавление пошло не по плану!---->")
            print(f"ERROR: {e}")


# async def add_users():
#     print("Добавляем стандартного юзера")
#
#     async with engine.begin() as conn:
#         try:
#             await conn.execute(
#                 text("INSERT INTO users (hashed_password, login, email, role_id, ggp_percent_begin, ggp_percent_end, "
#                      "sub_ggp_percent, sub_offline, sub_ggp, registered_at, is_active) VALUES ("
#                      "'$2b$12$bQ/w7vHbxqmuzQIusdwMvOvfhuu2ChGjcU51CLuqZw4cgYiPh8Vs.', 'def_admin@example.com', "
#                      "'string', 1, 100, 150, True, False, False, '2023-11-10 21:14:43.681332', True);"
#                 )
#             )
#
#         except Exception as e:
#             print("<----Добавление User ошибка не по плану!---->")
#             print(f"ERROR: {e}")


asyncio.run(add_roles())
