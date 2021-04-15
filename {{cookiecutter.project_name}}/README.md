# {{cookiecutter.project_name}}

This repo contains all the code of the website from https://{{cookiecutter.domain}}

### Development

Uses the default Django development server.

1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000). The "app" folder is mounted into the container and your code changes apply automatically.

### Production

Uses gunicorn + nginx.

1. Build the images and run the containers:

    ```sh
    $ docker-compose -f docker-compose.prod.yml up --build
    ```

    Test it out at [http://localhost:1337](http://localhost:1337). No mounted folders. To apply changes, the image must be re-built.

    NOTE: If you run the Development environment and then you run the production environment you will get a error that says that the yachtty_pro database is not created:
    ```sh
    $ docker-compose up -d --build
    ...
    $ docker-compose -f docker-compose.prod.yml up -d --build
    ...
    web_1    |   File "/usr/local/lib/python3.6/site-packages/psycopg2/__init__.py", line 127, in connect
    web_1    |     conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
    web_1    | django.db.utils.OperationalError: FATAL:  database "{{cookiecutter.postgresql_database}}_prod" does not exist
    ```
    This happens because the database is created the first time that the db service is started. In order to "restart" the db service you have to stop the docker-compose with:

    ```sh
    $ docker-compose down --volumes
    $ docker-compose -f docker-compose.prod.yml down --volumes
    ```