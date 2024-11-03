### To set up and run your application using Docker, follow these steps:

- Create a virtual environment:
  ```bash
  python -m venv venv
  ```
- Activate the virtual enviroment:
  ```bash
  source venv/bin/activate
  ```
- Change to the `app/` directory:

  ```bash
  cd app/
  ```

- Build and start the containers:
  ```bash
  docker-compose up --build
  ```
- Create migrations for any changes in the models:

  ```bash
  docker-compose exec web python manage.py makemigrations
  ```

- Apply database migrations:
  ```bash
  docker-compose exec web python manage.py migrate
  ```
- Start Django server:
  ```bash
  python manage.py runserver
  ```

Once everything is up and running, you should be able to access your
application at `http://localhost:8000`. You can access various endpoints
with the path `/api/manage_name/`.
