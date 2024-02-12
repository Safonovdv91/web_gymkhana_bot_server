from sqladmin import ModelView

from src.roles.models import Role
from src.sport_classes.models import SportClass
from src.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.registered_at, User.role]
    column_details_exclude_list = [User.hashed_password]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    category = "accounts"
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True


class RoleAdmin(ModelView, model=Role):
    name = "Роль"
    name_plural = "Роли"
    icon = "fa-solid fa-address-book"
    column_list = [Role.id, Role.name, Role.description, Role.users]
    can_delete = False


class SportClassAdmin(ModelView, model=SportClass):
    name = "Спорт-класс"
    name_plural = "Спортивные классы"
    icon = "fa fa-free-code-camp"
    column_list = [
        SportClass.id,
        SportClass.description,
        SportClass.sport_class,
        SportClass.users,
    ]
