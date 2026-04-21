# Веб-приложение «магазин для животных»

Учебный проект на Django. Сейчас сделана только внешняя часть: страницы, стили, переходы. Товары заданы в коде (файл `shop/data.py`), не в базе.

## Что внутри

- Django 5, приложение `shop`
- Страницы: главная, каталог (с фильтром по категории), карточка товара, о магазине, контакты
- Docker: образ на Python 3.12, запуск через gunicorn

## Запуск без Docker

Нужен Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/

## Запуск с Docker

```bash
docker compose up --build
```

Сайт: http://127.0.0.1:8000/

Для продакшена нужно задать свои `DJANGO_SECRET_KEY` и `DJANGO_ALLOWED_HOSTS` (через переменные окружения в compose или хостинге).

## Файлы для научрука

`DOKUMENTACIYA_NAUCHRUK.md` — описание проекта, сценарии, глоссарий.
# animal-shop
# animal-shop
# animal-shop
# animal-shop
# animal-shop
