from src.users.repository import UserRepository


class UserService:
    @classmethod
    def lst(cls):
        users = UserRepository.lst()
        print(users)