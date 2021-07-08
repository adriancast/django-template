# {{cookiecutter.project_name}}

This repo contains all the code of the website from https://{{cookiecutter.domain}}

### Development

Uses the default Django development server.

1. Check that you have your .env.dev and .env.dev.db.  If for some reason these files are not generated, remember that you can find samples in the repository.
   ```sh
   $ cat .env.dev
   
   DEBUG=1
   SECRET_KEY={{cookiecutter.secret_key}}
   DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
   SQL_ENGINE=django.db.backends.postgresql
   SQL_DATABASE={{cookiecutter.postgresql_database}}_dev
   SQL_USER={{cookiecutter.postgresql_user}}
   SQL_PASSWORD={{cookiecutter.postgresql_password_dev}}
   SQL_HOST=db
   SQL_PORT=5432
   DATABASE=postgres
   
   $ cat .env.dev.db

   POSTGRES_USER={{cookiecutter.postgresql_user}}
   POSTGRES_PASSWORD={{cookiecutter.postgresql_password_dev}}
   POSTGRES_DB={{cookiecutter.postgresql_database}}_dev
    ```

2. Create docker volumes to save the data:
    ```sh
    $ docker volume create --name={{cookiecutter.project_name}}_postgres_data_dev
    {% if cookiecutter.add_prometheus_and_grafana == 'yes' %}$ docker volume create --name={{cookiecutter.project_name}}_grafana{% endif %}
    ```

3. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.

### Production

Uses Gunicorn + Nginx + Letsencrypt.

1. Check that you have your {% if cookiecutter.add_prometheus_and_grafana == 'yes' %}.env.prod.grafana, {% endif %}.env.prod, .env.prod.db and .env.prod.proxy-companion. If for some reason these files are not generated, remember that you can find samples in the repository.
    ```sh
    $ cat .env.prod
    $ cat .env.prod.db
    $ cat .env.prod.proxy-companion
    {% if cookiecutter.add_prometheus_and_grafana == 'yes' %}$ cat .env.prod.grafana{% endif %}
    ```
2. Create docker volumes to save the data
    ```sh
    $ docker volume create --name={{cookiecutter.project_name}}_postgres_data
    $ docker volume create --name=static_volume
    $ docker volume create --name=media_volume
    $ docker volume create --name=certs
    $ docker volume create --name=html
    $ docker volume create --name=vhost
    {% if cookiecutter.add_prometheus_and_grafana == 'yes' %}$ docker volume create --name={{cookiecutter.project_name}}_grafana{% endif %}
    ```
3. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up --build
    ```

# Hints to work with this project

1. Execute a command inside de Django container in **DEVELOPMENT** environment.
    ```sh
    $ docker-compose exec web python manage.py shell
    ```
2. Execute a command inside de Django container in **PRODUCTION** environment.
    ```sh
    $ docker-compose -f docker-compose.prod.yml exec web python manage.py shell
    ```
3. Create Django migrations. In case you want to execute this in production environment, remember to use the -f parameter.
    ```sh
    $ docker-compose exec web python manage.py makemigrations
    ```
4. Execute Django migrations. In case you want to execute this in production environment, remember to use the -f parameter.
    ```sh
    $ docker-compose exec web python manage.py migrate
    ```
   
5. Create Django admin superuser. In case you want to execute this in production environment, remember to use the -f parameter.
    ```sh
    $ docker-compose exec web python manage.py createsuperuser
    ```
6. To configure the debugger in Pycharm you can use guide in the following [link](https://testdriven.io/blog/django-debugging-pycharm/#:~:text=To%20do%20so%2C%20open%20PyCharm,create%20a%20new%20Docker%20configuration.). Remember that you must have a professional license to use this feature.