### REST API для книжного магазина на FastAPI с PostgreSQL
```Учебный проект```
# Стек технологий

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0 (async)
- Alembic
- Pydantic v2
- JWT аутентификация

# Структура проекта

```
app/
├── main.py           # Точка входа
├── config.py         # Настройки
├── database.py       # Подключение к БД
├── models.py         # SQLAlchemy модели
├── schemas.py        # Pydantic схемы
├── crud.py           # Функции работы с БД
├── security.py       # JWT и хеширование паролей
├── dependencies.py   # FastAPI зависимости
└── routers/
    ├── auth.py       # Аутентификация
    ├── books.py      # Книги
    ├── authors.py    # Авторы
    └── orders.py     # Заказы
```

# Старт

## Локально (без Docker)
```
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Установить зависимости
pip install -r requirements.txt

# Настроить переменные окружения
cp .env.example .env
# Отредактировать .env, указав DATABASE_URL для локальной PostgreSQL

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload
```

# API Endpoints

## Аутентификация

| Метод | Endpoint       | Описание                 |
| ----- | -------------- | ------------------------ |
| post  | /auth/register | Регистрация пользователя |
| post  | /auth/login    | Вход                     |
## Книги

|Метод|Endpoint|Описание|Доступ|
|---|---|---|---|
|GET|/books|Список книг (пагинация, фильтрация)|Все|
|GET|/books/{id}|Информация о книге|Все|
|POST|/books|Добавить книгу|Admin|
|PATCH|/books/{id}|Обновить книгу|Admin|
|DELETE|/books/{id}|Удалить книгу|Admin|

## Авторы

|Метод|Endpoint|Описание|Доступ|
|---|---|---|---|
|GET|/authors|Список авторов|Все|
|GET|/authors/{id}|Автор с его книгами|Все|
|POST|/authors|Создать автора|Admin|

## Заказы

|Метод|Endpoint|Описание|Доступ|
|---|---|---|---|
|POST|/orders|Оформить заказ|Авторизованные|

# Переменные окружения


|Переменная|Описание|По умолчанию|
|---|---|---|
|DATABASE_URL|URL подключения к PostgreSQL|postgresql+asyncpg://postgres:postgres@db:5432/bookstore|
|SECRET_KEY|Секретный ключ для JWT|dev-secret-key-change-me|
|ALGORITHM|Алгоритм JWT|HS256|
|ACCESS_TOKEN_EXPIRE_MINUTES|Время жизни токена|30|
