FROM python:3.14.0a1-bookworm

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r docker/requirements.txt

EXPOSE 8000

CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]

