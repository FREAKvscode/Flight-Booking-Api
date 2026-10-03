# Flight Booking API

API сервиса бронирования и заказа авиабилетов «Просто лететь».
Тестовое задание на позицию Backend-разработчика.

---

## Стек

- Python 3.11
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL 15
- Alembic
- Pydantic v2
- JWT (python-jose)
- passlib + bcrypt
- Docker / Docker Compose
- Postman

---

## Роли пользователей

| Роль | Возможности |
|---|---|
| Гость | Регистрация, логин, просмотр списка билетов |
| Клиент | Всё то же + корзина, оформление заказов, редактирование профиля |
| Администратор | Всё то же + CRUD авиабилетов (создание, редактирование, удаление) |

---

## Быстрый запуск через Docker

### Требования

- Docker Desktop (установленный и запущенный)
- Git

### Шаги

Открой терминал (PowerShell, CMD или bash) и выполни команды:

```bash
# 1. Перейти в папку, где будет храниться проект (пример для Windows)
cd C:\Users\%USERNAME%\PycharmProjects

# Для Linux/Mac:
# cd ~/PycharmProjects

# 2. Клонировать репозиторий (создастся папка Flight-Booking-Api)
git clone https://github.com/FREAKvscode/Flight-Booking-Api.git

# 3. Перейти в папку с docker-compose.yml
cd Flight-Booking-Api/deploy

# 4. Собрать и запустить контейнеры
docker-compose up --build
```

После запуска в терминале появятся логи:

```
flight-db   | database system is ready to accept connections
flight-app  | INFO  [alembic.runtime.migration] Running upgrade -> ..., init
flight-app  | Seed OK
flight-app  | INFO:     Uvicorn running on http://0.0.0.0:8000
```

Что происходит автоматически:

1. Собирается образ приложения из `project/Dockerfile`.
2. Скачивается и запускается PostgreSQL 15.
3. Применяются миграции Alembic (создаются таблицы).
4. Загружаются seed-данные: админ, клиент, тестовые билеты.
5. Запускается FastAPI-сервер на порту 8000.

### Проверка работы

Открой в браузере:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Остановка

В терминале, где запущен `docker-compose`, нажми `Ctrl+C`. Затем:

```bash
docker-compose down
```

Флаг `-v` (например, `docker-compose down -v`) удалит volume с данными БД.

---

## Тестовые аккаунты

Создаются автоматически при первом запуске (seed).

| Роль | Email | Пароль |
|---|---|---|
| Администратор | admin@flight.ru | QWEasd123 |
| Клиент | user@flight.ru | password |

---

## Тестирование через Swagger

1. Открой http://localhost:8000/docs

2. Выполни `POST /api-flight/login` с телом:

   ```json
   {
     "email": "admin@flight.ru",
     "password": "QWEasd123"
   }
   ```

3. Скопируй значение `user_token` из ответа.

4. Нажми кнопку Authorize в правом верхнем углу страницы.

5. Вставь токен без префикса `Bearer` — Swagger добавит его автоматически.

   Правильно: `eyJhbGciOiJIUzI1NiIs...`
   Неправильно: `Bearer eyJhbGciOiJIUzI1NiIs...`

6. Нажми Authorize, затем Close.

7. Теперь все защищённые эндпоинты (помечены замком) работают.

### Порядок тестирования

1. `POST /api-flight/login` — получить токен.
2. Authorize — вставить токен.
3. `GET /api-flight/products` — список билетов.
4. `POST /api-flight/cart/1` — добавить билет в корзину.
5. `GET /api-flight/cart` — просмотр корзины.
6. `POST /api-flight/order` — оформить заказ.
7. `GET /api-flight/order` — история заказов.

---

## Postman-коллекция

Файл: `collection/flight_api_postman_collection.json`

### Импорт

1. Открой Postman.
2. File, затем Import, выбери файл `collection/flight_api_postman_collection.json`.
3. Коллекция `flight-api` появится в левой панели.

### Использование

1. В коллекции настроена переменная `host` = `http://localhost:8000/api-flight`.
2. Отправь запрос `login` — токен автоматически сохранится в переменную `{{token}}`.
3. Остальные запросы подхватят токен через Bearer Auth на уровне коллекции.

### Что внутри

14 запросов, покрывающих все эндпоинты:

- login, signup
- get products, create product, update product, delete product
- get profile, update profile, logout
- add to cart, get cart, delete from cart
- create order, get orders

---

## Структура проекта

```
.
├── collection/                          # Postman-коллекция
│   └── flight_api_postman_collection.json
│
├── deploy/                              # Docker-инфраструктура
│   └── docker-compose.yml               # Postgres + FastAPI
│
├── project/                             # Исходный код приложения
│   ├── alembic/                         # Миграции
│   │   ├── versions/                    # Файлы миграций
│   │   ├── env.py                       # Настройка Alembic
│   │   └── script.py.mako               # Шаблон миграций
│   ├── app/
│   │   ├── api/                         # Эндпоинты (роутеры)
│   │   │   ├── auth.py                  # /signup, /login
│   │   │   ├── cart.py                  # /cart
│   │   │   ├── deps.py                  # Зависимости (auth)
│   │   │   ├── order.py                 # /order
│   │   │   ├── products.py              # /products, /product
│   │   │   └── profile.py               # /profile, /logout
│   │   ├── core/                        # Ядро приложения
│   │   │   ├── config.py                # Настройки из .env
│   │   │   └── security.py              # JWT + хеши паролей
│   │   ├── db/                          # Работа с БД
│   │   │   ├── all_models.py            # Импорт всех моделей
│   │   │   ├── base.py                  # DeclarativeBase
│   │   │   ├── init_db.py               # Seed-данные
│   │   │   └── session.py               # SessionLocal, get_db
│   │   ├── models/                      # SQLAlchemy-модели
│   │   │   ├── cart.py
│   │   │   ├── order.py
│   │   │   ├── product.py
│   │   │   └── user.py
│   │   ├── schemas/                     # Pydantic-схемы
│   │   │   ├── product.py
│   │   │   └── user.py
│   │   └── main.py                      # Точка входа FastAPI
│   ├── alembic.ini
│   ├── Dockerfile
│   └── requirements.txt
│
└── README.md
```

---

## Эндпоинты API

Все эндпоинты имеют префикс `/api-flight`.

### Auth

| Метод | URL | Описание | Доступ |
|---|---|---|---|
| POST | `/signup` | Регистрация | Гость |
| POST | `/login` | Авторизация | Гость |

### Profile

| Метод | URL | Описание | Доступ |
|---|---|---|---|
| GET | `/profile` | Просмотр профиля | Авторизованные |
| PATCH | `/profile` | Редактирование профиля | Авторизованные |
| GET | `/logout` | Выход | Авторизованные |

### Products

| Метод | URL | Описание | Доступ |
|---|---|---|---|
| GET | `/products` | Список билетов | Все |
| POST | `/product` | Создать билет | Админ |
| PATCH | `/product/{id}` | Обновить билет | Админ |
| DELETE | `/product/{id}` | Удалить билет | Админ |

### Cart

| Метод | URL | Описание | Доступ |
|---|---|---|---|
| POST | `/cart/{product_id}` | Добавить в корзину | Клиент |
| GET | `/cart` | Просмотр корзины | Клиент |
| DELETE | `/cart/{item_id}` | Удалить из корзины | Клиент |

### Orders

| Метод | URL | Описание | Доступ |
|---|---|---|---|
| POST | `/order` | Оформить заказ | Клиент |
| GET | `/order` | История заказов | Клиент |

---

## Форматы ошибок

Все ошибки возвращаются в формате JSON.

| Код | Когда возникает | Пример тела |
|---|---|---|
| 401 | Неверный логин или пароль | `{"password": "Login failed"}` |
| 403 | Нет прав | `{"message": "Forbidden for you"}` |
| 403 | Невалидный токен | `{"message": "Login failed"}` |
| 404 | Ресурс не найден | `{"message": "Not found"}` |
| 422 | Ошибка валидации | `{"message": "Validation error", "field": "Validation error"}` |

---

## Разработка без Docker

### Запуск БД

```bash
cd deploy
docker-compose up -d db
```

### Локальный запуск приложения

```bash
# Перейти в папку проекта
cd project

# Создать и активировать виртуальное окружение
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/Mac

# Установить зависимости
pip install -r requirements.txt

# Создать файл .env в папке project со следующим содержимым:
# DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/flight_db
# SECRET_KEY=secret_key
# ALGORITHM=HS256
# ACCESS_TOKEN_EXPIRE_MINUTES=30

# Применить миграции
alembic upgrade head

# Загрузить seed-данные
python -m app.db.init_db

# Запустить сервер
uvicorn app.main:app --reload --port 8000
```

Сервер будет доступен по адресу http://localhost:8000/docs.

---

## Переменные окружения

Файл `project/.env` (не коммитится в git):

| Переменная | Описание | Пример |
|---|---|---|
| DATABASE_URL | URL подключения к PostgreSQL | `postgresql+psycopg2://user:password@localhost:5432/flight_db` |
| SECRET_KEY | Ключ для подписи JWT | `secret_key` |
| ALGORITHM | Алгоритм JWT | `HS256` |
| ACCESS_TOKEN_EXPIRE_MINUTES | Время жизни токена (мин.) | `30` |

При запуске через Docker переменные задаются в `docker-compose.yml` (секция `environment`), а не в `.env`.

