from sqlalchemy import text
import asyncio

from sqlalchemy.exc import SQLAlchemyError

from logger.logger import logger
from src.database import engine


async def add_sport_class(sport_class, description):
    logger.info(f"Adding sport_class: {sport_class}| [{description}]")
    async with engine.begin() as conn:
        try:
            await conn.execute(
                text(
                    f"INSERT INTO sport_classes (sport_class, description) VALUES('{sport_class}','{description}')"
                )
            )
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: "
                logger.error(msg=msg, exc_info=True)
            else:
                msg = "Unknown Exc: "
                msg += "add standard roles and sport-class error!"
                logger.error(msg=msg, exc_info=True)


async def add_role(role_name, description):
    logger.info(f"Adding role: {role_name}| [{description}]")
    async with engine.begin() as conn:
        try:
            await conn.execute(
                text(
                    f"INSERT INTO roles (name, description) VALUES('{role_name}','{description}')"
                )
            )
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg = "Database Exc: "
                logger.error(msg=msg, exc_info=True)
            else:
                msg = "Unknown Exc: "
                msg += "add standard roles and sport-class error!"
                logger.error(msg=msg, exc_info=True)


async def add_default_values():
    logger.info("Adding default values")

    DEFAULT_SPORT_CLASSES = {
        "A": "Best of the best",
        "B": "Sportsman speed rate: 100-105%",
        "C1": "Sportsman speed rate: 105-110%",
        "C2": "Sportsman speed rate: 110-115%",
        "C3": "Sportsman speed rate: 115-120%",
        "D1": "Sportsman speed rate: 120-130%",
        "D2": "Sportsman speed rate: 130-140%",
        "D3": "Sportsman speed rate: 140-150%",
        "D4": "Sportsman speed rate: 150-160%",
        "N": "Sportsman speed rate: 160+%",
    }

    DEFAULT_ROLES ={
        "Owner": "Can change role all users/admins, delete or create",
        "Admin": "Administrator can del users, and change user's settings",
        "User": "Can only change himself settings",
        "Guest": "Unknown person, can nothing",
    }

    logger.info("Adding roles ...")
    for k,v in DEFAULT_ROLES.items():
        await add_role(k, v)
    logger.info("Adding DEFAULT ROLES complete! success")

    logger.info("Adding sport_classes...")
    for k,v in DEFAULT_SPORT_CLASSES.items():
        await add_sport_class(k, v)
    logger.info("Adding DEFAULT SPORT CLASSES complete! success")

asyncio.run(add_default_values())
