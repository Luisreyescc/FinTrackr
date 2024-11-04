FROM python:3.14.0a1-bookworm

WORKDIR /app

COPY app /app

RUN pip install django mysqlclient python-decouple djangorestframework django-cors-headers

EXPOSE 8000

CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]

