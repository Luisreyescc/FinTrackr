### To set up and run your application using Docker, follow these steps

- Build and start the containers:

  ```bash
  docker-compose up --build
  ```

- Open another terminal
- Create migrations for any changes in the models:

  ```bash
  docker-compose exec web python /app/fintrackr/manage.py makemigrations
  ```

- Apply database migrations:

  ```bash
  docker-compose exec web python /app/fintrackr/manage.py migrate
  ```

  Once everything is up and running, you should be able to access your
  application at `http://localhost:8000`. You can access various endpoints
  with the path `/api/manage_name/`.
