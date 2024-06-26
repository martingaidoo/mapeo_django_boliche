# mapeo_django_boliche

Requisitos:
Instalar Docker y docker compose para poder realizar el tutorial.

Tutorial para instalar Django [Turorial de Django!](https://docs.djangoproject.com/en/2.0/intro/tutorial01/)
Tutorial para crear un entorno virtual de python [Tutorial para crear entorno virtual](https://docs.djangoproject.com/en/2.0/intro/contributing/)

---
# Crear un proyecto generico 
Creamos la carpeta donde generaremos nuestra **`app`**. Por ejemplo `proyecto`.
```sh
mkdir proyecto
cd proyecto/
```

Creamos el archivo **`requirements.txt`** para instalar las dependencias en el contenedor, y agregamos lo siguiente.
```
#Framework Django
Django
#Librería para la conexión con PostgreSQL
psycopg2-binary
```

Creamos el archivo **`Dockerfile`** para generar el contenedor donde almacenamos la **`app`**.
```
# Etapa de construcción
FROM python:3.12-alpine AS base
LABEL maintainer="Luciano Parruccia <parruccia@yahoo.com.ar>"
LABEL version="1.0"
LABEL description="cloudset"
RUN apk --no-cache add bash pango ttf-freefont py3-pip curl

# Etapa de construcción
FROM base AS builder
# Instalación de dependencias de construcción
RUN apk --no-cache add py3-pip py3-pillow py3-brotli py3-scipy py3-cffi \
  linux-headers autoconf automake libtool gcc cmake python3-dev \
  fortify-headers binutils libffi-dev wget openssl-dev libc-dev \
  g++ make musl-dev pkgconf libpng-dev openblas-dev build-base \
  font-noto terminus-font libffi

# Copia solo los archivos necesarios para instalar dependencias de Python
COPY ./requirements.txt .

# Instalación de dependencias de Python
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt \
  && rm requirements.txt

# Etapa de producción
FROM base
RUN mkdir /code
WORKDIR /code
# Copia solo los archivos necesarios desde la etapa de construcción
COPY ./requirements.txt .
RUN pip install -r requirements.txt \
  && rm requirements.txt
COPY --chown=user:group --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages 
#COPY --from=build-python /usr/local/bin/ /usr/local/bin/
ENV PATH /usr/local/lib/python3.12/site-packages:$PATH
# Configuración adicional
RUN ln -s /usr/share/zoneinfo/America/Cordoba /etc/localtime

# Comando predeterminado
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "app.wsgi"]

```

Creamos el archivo **`.env.db`** para almacenar las variables del entorno.
```
#Definimos cada variable
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=postgres
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
# Configuración para inicializar postgres
POSTGRES_PASSWORD=${DATABASE_PASSWORD}
PGUSER=${DATABASE_USER}
PGADMIN_DEFAULT_EMAIL=postgres@postgresql.com
PGADMIN_DEFAULT_PASSWORD=${DATABASE_PASSWORD}
```

Creamos el archivo **`docker compose.yml`** para manipular los contenedores
```
services:
  db:
    image: postgres:alpine
    env_file:
      - .env.db
    environment:
      - POSTGRES_INITDB_ARGS=--auth-host=md5 --auth-local=trust
    healthcheck:
      test: [ "CMD-SHELL", "pg_isready" ]
      interval: 10s
      timeout: 2s
      retries: 5
    volumes:
      - postgres-db:/var/lib/postgresql/data
    networks:
      - net

  backend:
    build: .
    container_name: proyecto_app
    command: runserver 0.0.0.0:8000
    entrypoint: python3 manage.py
    env_file:
      - .env.db
    expose:
      - "8000"
    ports:
      - "8000:8000"
    volumes:
      - ./src:/code
    depends_on:
      db:
        condition: service_healthy
    networks:
      - net

  generate:
    build: .
    command: bash -c 'mkdir src && django-admin startproject app src'
    env_file:
      - .env.db
    volumes:
      - .:/code
    depends_on:
      - db
    networks:
      - net

  manage:
    build: .
    entrypoint: python3 manage.py
    env_file:
      - .env.db
    volumes:
      - ./src:/code
    depends_on:
      - db
    networks:
      - net

networks:
  net:


volumes:
  postgres-db:
```

## Pasos iniciales para comenzar a trabajar con Django.

Migro la base de datos que se crea por defecto para el proyecto.
```sh
docker compose run manage migrate
```
Para generar un súper usuario de Django
```sh
docker compose run manage createsuperuser
```
Iniciamos los contenedores de la aplicación. El comando ***`-d`*** es para ejecutarlo como demonio, si queremos ir viendo el log de los contenedores, eliminamos el ***`-d`***
```sh
docker compose up -d backend
```
Para ingresar a la app accedemos al siguiente url [http://localhost:8000/admin/](http://localhost:8000/admin/)

En caso de tener algún problema, podemos ver el log de los contenedores. Reemplazamos **`nombre`** por el nombre de la app que creamos.
```sh
docker logs -f nombre_app_1
docker logs -f nombre_db_1
```
---
## Comandos útiles.
Para generar las modificaciones de la base de datos ejecutamos:
```sh
docker compose run manage makemigrations
docker compose run manage migrate
```
Para borrar los contenedores del proyecto:
```sh
docker compose down
```
Para el caso que deseamos eliminar todo lo generado por el docker compose, siempre y cuando los contenedores no estén iniciados, ejecutamos:
```sh
docker system prune -a
```
En el caso de tener problemas para modificar o eliminar algún archivo, le cambiamos el propietario con el siguiente comando, y reemplazamos **`user`** por el usuario con el que estamos logueado
```sh
sudo chown $USER:$USER -R .
```
---
## Editando los archivos de la APP

### **`models.py`**
### **`admin.py`**

## Realizamos las migraciones a la base de datos y creamos el super usuario.
```sh
docker compose run --rm manage makemigrations
docker compose run --rm manage migrate
```
## Creamos el fixture
Creamos la carpeta dentro del directorio de la aplicación **`fixtures`** y dentro el siguiente archivo
### **`initial_data.json`**

## Cargamos los datos con el siguiente comando
```
docker compose run --rm manage loaddata initial_data
```