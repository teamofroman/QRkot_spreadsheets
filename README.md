# Проект QRKot

Приложение для Благотворительного фонда поддержки котиков **QRKot**.

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

# Установка и запуск проекта
## Клонирование проекта

```bash
git clone ...
```

## Создание и активация виртуального окружения

- Linux
```bash
python3 -m venv venv
source ./venv/bin/activate
```

- Windows
```cmd
python -m venv venv
./venv/Scripts/activate.bat
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

# Запуск проекта
## Первоначальная настройка
Перед первым запуском создать в корне проекта файл `.env` и задать значения 
следующим ключам:
- `DATABASE_URL` - строка подключения к базе данных в формате 
  `driver://user:pass@localhost/dbname`. По умолчанию - `sqlite+aiosqlite:///./fastapi.db`
- `SECRET` - секретная строка (набор символов) для генерации токенов. По 
  умолчанию - `SECRERT`
- `FIRST_SUPERUSER_EMAIL` - email автоматически создаваемого администратора
- `FIRST_SUPERUSER_PASSWORD` - его пароль
- `CREATE_SAMPLE_DATA` - создавать тестовые данные (True) или нет (False)

Данные для доступа к GoogleAPI
- `TYPE`
- `PROJECT_ID`
- `PRIVATE_KEY_ID`
- `PRIVATE_KEY`
- `CLIENT_EMAIL`
- `CLIENT_ID` 
- `AUTH_URI`
- `TOKEN_URI`
- `AUTH_PROVIDER_X509_CERT_URL`
- `client_x509_cert_url`
- `UNIVERSE_DOMAIN`

Пользователь (его e-mail), которому дается доступ к создаваемым GoogleSheets
- `EMAIL`

Если не указывать `FIRST_SUPERUSER_EMAIL` и `FIRST_SUPERUSER_PASSWORD`, то 
администратор не создается и его надо создать вручную.

## Подготовка базы данных

При первом запуске выполнить команду:
```bash
alembic update head
```

## Запуск приложения

```bash
uvicorn app.main:app
```

# Технологии

- python 3.9
- FastAPI 0.78.0
- FastAPIUser 10.0.4
- SQLAlchemy 1.4.36
