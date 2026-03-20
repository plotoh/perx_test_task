# test_service

core-модуль для fastapi‑приложения, c интерфейсами для работы с postgresql и redis

выбрал clean architecture - больше подходит под требования, выбирал из fsd, микросервисной, cba
## архитектура

- **core** - инфраструктурное ядро (di, lifespan, config by pydantic, подключение к бд, редису, конфиг, логи, ошибки, зависимости)
- **example** - показывает, как остальные модули могут использовать core

## паттерны
- **Repository**
- **Dependency Injection**
- **Singleton** для конфига и редиса
- **Lifespan**
- **базовый layered + clean architecture** легко адаптируемый под более специфичные архитекруты

## структура

```text
perx_architecture/
├── app
│   ├── core
│   │   ├── database
│   │   │   ├── repositories
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py
│   │   │   │   └── sqlalchemy.py
│   │   │   └── __init__.py
│   │   ├── exceptions
│   │   │   ├── __init__.py
│   │   │   └── handlers.py
│   │   ├── middlewares
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   ├── lifespan.py
│   │   ├── logging.py
│   │   └── redis.py
│   ├── example
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   └── users.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── repositories
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   └── __init__.py
│   ├── __init__.py
│   └── main.py
├── migrations
├── tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_database.py
│   └── test_repo.py
├── alembic.ini
├── docker-compose.yml
└── pyproject.toml
```
## замечания

- **улучшить логирование и больше самописных исключений** (инфомрация, треккинг медленных запросов и т.п.)

- **более умный кэш** - можно добавить библиотеку fastapi-cache или свою обёртку с сериализацией pydantic моделей чтобы не писать json.dumps в каждом сервисе

- **тесты** – бязательно протестировать подключение к БД и Redis, работу репозитория и т.п.

- **pre-commit хуки** - перед каждым коммитом прогонять ruff, mypy, black

- **кэширование config.py**

- **другой клиент рэдиса**

- **В целом универсальный шаблон, его легко переделать под ddd esa cda и т.д, но базово он закрывает все запросы из ТЗ **

- **в нескольких папках вместо файла прописал логику в __init__, можно вынести в файл, но пока не имеет смысла**

- **возможно лишняя абстракция для репозиториев, но не вижу в этом значимой проблемы**

