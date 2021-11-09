# {{cookiecutter.project_name}}

This repo contains all the code of the website from https://{{cookiecutter.production_domain_url}}

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
    {% if cookiecutter.add_prometheus_and_grafana == 'yes' %}Grafana dashboard will be accesible in [http://localhost:3000](http://localhost:3000).{% endif %}

### Before deploying to production
It's important that the DNS records are setup properly before deploying the app to the production server. You will need to make sure that you have the following records:
- A: record to set the IPv4 of your production server
- AAAA: record to set the IPv6 of your production server
- CNAME: record to configure the "wwww" subdomain.

Here is an example of how to configure this in [GoDaddy](https://godaddy.com/)
![Screenshot from 2021-07-11 19-28-45](https://user-images.githubusercontent.com/17761956/125204570-40738000-e27e-11eb-81a4-7a495949af73.png)


### Production configuration

You will have to configure the production server, the Dockerhub account, Github actions for the CI/CD and the .env files in the production server:

* Dockerhub: You must create an [access token](https://docs.docker.com/docker-hub/access-tokens/) to download the Docker images from the production server. Thenm you must create the following repositories in your Docker Hub account:
  * {{cookiecutter.project_name}}
  * {{cookiecutter.project_name}}-nginx
{% if cookiecutter.add_prometheus_and_grafana == 'yes' %}
  * {{cookiecutter.project_name}}-prometheus
  * {{cookiecutter.project_name}}-grafana
{% endif %}

* Github actions: You must enable Github actions in your Github repository and add the required secrets inside Github
  * Enable actions inside Reposirory > Settings > Actions > Actions permissions > Allow all actions
  * Create the following secrets inside Reposirory > Settings > Secrets
    * DOCKERHUB_USERNAME: Username of your Docker Hub.
    * DOCKERHUB_TOKEN: Access token generated previously in Docker Hub.
    * SSH_PRIVATE_KEY: Generated RSA private key. This will be used to deploy the code in the server.
    * SSH_PUBLIC_KEY: Generated RSA public key. This will be used to deploy the code in the server.
 * Production server: For this example we will be using [Digital Ocean](https://www.digitalocean.com/). Digital Ocean provides with droplets with Docker pre-installed. For an easy installation, I really recommend you to use those droplets. ![image](https://user-images.githubusercontent.com/17761956/140977706-ac9abf8f-931d-41e1-9908-218879b4b2b2.png)
. While creating the server, you need to specify that the SSH public key generated before is trusted. To do this, you need to add the SSH public key in the end of the ~/.ssh/authorized_keys file.

    ```sh
      echo "ssh-rsa EXAMPLEzaC1yc2E...GvaQ== username@203.0.113.0" >> ~/.ssh/authorized_keys
    ```
    You can automate this task inside Digital Ocean using the "User data" option while creating the droplet.
    ![image](https://user-images.githubusercontent.com/17761956/140977992-e6ea2b6e-69bb-4b17-a86b-476de166e74e.png)

 * Environment files: Once the server is created, remember that you must add the .env files inside /opt/{{cookiecutter.project_name}}.
    ```sh
    $ cat .env.prod
    $ cat .env.prod.db
    $ cat .env.prod.proxy-companion
    {% if cookiecutter.add_prometheus_and_grafana == 'yes' %}$ cat .env.prod.grafana{% endif %}
    ```
{% if cookiecutter.add_prometheus_and_grafana == 'yes' %}
# Configuring Grafana in production
It will automatically load the provisioning configurations and serve the dashboard in [http://{{cookiecutter.production_domain_url}}:3000](http://{{cookiecutter.production_domain_url}}:3000).
{% endif %}

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
