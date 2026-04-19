FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=0
ENV DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,web

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput && python manage.py migrate --noinput

EXPOSE 8000

CMD ["gunicorn", "pet_store.wsgi:application", "--bind", "0.0.0.0:8000"]
