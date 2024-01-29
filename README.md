# Gymkhana bot webserver!
Web server for setting gymkhana bot!!!( in developing )
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

## Инструкция по запуску(Для фронта)
После запуска можно вносить все изменения в папке frontend - заниматься версткой и все будет отображаться сразу после внесенных именений
### Вручную:
Должна крутиться БД на localhost:5432, в соответствии с .env данными. Если базы нет то лучше сразу запустить через докер-композ.

1. Активируем виртуальное окружение
   Открывает терминал в папке с проектом и вбиваем команду
   >venv\Scripts\Activate.ps1
   появится зеленая приписка в терминале.
2. Запустить backend сервер
   > uvicorn src.main:app --reload
3. Останвить сервер: *Ctrl + C*
   ### возможные сложности
   нет папки venv
   > python -m venv venv
  или
   > python3.11 -m venv venv
### Через докер
1. запустить докер контейнеры
> docker compose up -d
2. Остановить
> docker compose down
> docker rmi web_

