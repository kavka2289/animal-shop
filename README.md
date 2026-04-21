# Веб-приложение «магазин для животных»

Проект на Django.

## Что внутри

- Django 5, приложение `shop`
- Страницы: главная, каталог (с фильтром по категории), карточка товара, о магазине, контакты
- Docker: образ на Python 3.12

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Запуск с Docker

```bash
docker compose up --build
```

Сайт: http://127.0.0.1:8000/

## Файлы для научрука

`DOKUMENTACIYA_NAUCHRUK.md` — описание проекта, сценарии, глоссарий.