import json

from faker import Faker


class FakeUser:
    def __init__(self, user_id: int):
        fake = Faker()
        self.user_id = user_id
        self.email = fake.email()
        self.ggp_percent_begin = fake.random_int(50, 130)
        self.ggp_percent_end = fake.random_int(self.ggp_percent_begin, 200)
        self.sub_ggp_percent = fake.boolean()
        self.sub_offline = fake.boolean()
        self.sub_ggp = fake.boolean()
        self.sub_world_record = fake.boolean()
        self.telegram_id = str(fake.random_int(1_000_000, 1_000_000_000))

    def __repr__(self):
        return f"{self.user_id}, {self.email}, {self.ggp_percent_begin}, {self.ggp_percent_end}," \
               f" {self.sub_ggp_percent}, {self.sub_offline}, {self.sub_ggp}, {self.sub_world_record}, {self.telegram_id}"

    def __str__(self):
        return self.__repr__()


users = (FakeUser(i) for i in range(5, 20))

for user in users:
    data = {
        "user_id": user.user_id,
        "email": user.email,
        "ggp_percent_begin": user.ggp_percent_begin,
        "ggp_percent_end": user.ggp_percent_end,
        "sub_ggp_percent": user.sub_ggp_percent,
        "sub_offline": user.sub_offline,
        "sub_ggp": user.sub_ggp,
        "sub_world_record": user.sub_world_record,
        "telegram_id": user.telegram_id
    }
print(data)
print(json.dumps(data))
for k, v in data.items():
    print(f"key: {k}, value: {v}")
