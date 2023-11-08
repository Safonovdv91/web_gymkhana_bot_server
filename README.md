# Gymkhana bot webserver!
Web server for setting gymkhana bot!!!
## Tech:
- FastApi
- pydantic
- postgresql
- alembic
- celery
- flower
- redis

### What does this project do?
  Создание веб-сервиса (сайта) с настройками и управлением уведомлений через телеграмм-бота.
  
### Why is this project useful?
  Сервис позволяет оперативно получать уведомление о результатах в спортивной дисциплине: мотоджимхана.
  
### How do I get started?
  if server working: go to url: (...) not now...
  
### Where can I get more help, if I need it?
  tg: @SoftikMy1
  Открыт для общения/предложений новых фич в проекте

### Project Structure
```
fastapi-project  
├── alembic/  
├──  src  
│   ├── auth  
│   │   ├── auth_config.py  # authentication config
│   │   ├── routers.py  
│   │   ├── schemas.py      # pydantic models  
│   │   ├── models.py       # db models User & Role  
│   │   └── utils.py  
│   ├── pages  
│   │   └──  routers.py     #file with routers pages
│   ├── templatese/     # html pages
│   │   ├──  base.html      # common part of html
│   │   ├──  getusers.html  # page get users & get users by id
│   │   ├──  not_exist.html # page error 404
│   ├── users  
│   │   ├── routers.py  
│   │   ├── schemas.py  # pydantic models  
│   │   └── models.py  
│   ├── config.py       # global configs  
│   ├── models.py       # global models  
│   ├── exceptions.py   # global exceptions  
│   ├── database.py     # db connection related stuff  
│   └── main.py  
├── tests/  
│   ├── conftest
│   ├── test_auth   # test "auth" endpoints
│   └── test_user   # test "users" endpoints
├── templates/  
├── .env  
├── env # example of .env   
├── .gitignore  
├── logging.ini  
├── docker-compose.yml # docker command for start Docker-conteiners  
└── alembic.ini
```
***
## Этап разработки
- [ ] Авторизация пользователя
- [ ] Подписку/отписку на любой спортивный класс(B,C1, D4) (чекбоксы)
- [ ] Подписку/отписку на оповещение мировых рекордов( чекбокс )
- [ ] Ввод данных на проценты от результата


