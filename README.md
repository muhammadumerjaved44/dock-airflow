# Easy way to install Apache Airflow

This image is bases on the linux debian latest and pull from the `continuumio/miniconda3`, heaving the Install the conda enviorment as `(base)`. This image also using the postgress database that helps to use run the air-flow services

## How to make the docker-compose file from this image

### Step 1: Install the Postgres database
Create a service for the postgres sql pull from the image `postgres:10.1-alpine`.

#### Postgres sql in docker-compose file
```
airflow-postgres:
    container_name: airflow-postgres
    image: postgres:10.1-alpine
    volumes:
      - ./postgres_data/:/var/lib/postgresql/data:rw
    ports:
      - 5438:5432
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
```

#### Create local variables in the .env file
```
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
```

or to use the EXPORT these variables

```
export POSTGRES_USER=airflow
export POSTGRES_PASSWORD=airflow
export POSTGRES_DB=airflow

```

#### To presist the data you can use volumes like this
```
-volumes:
    ./postgres_data/:/var/lib/postgresql/data:rw
```

### Step 2: Initialize the database for the Airflow
Apache require to run the migrations in the postgres database so that Airflow has to run the command `airflow initdb`. For this you have to create the separate service

#### airflow initdb
```
#  airflow initdb service configuration #1
  airflow-initdb:
    container_name: airflow-initdb
    build: .
    entrypoint: airflow initdb
    depends_on:
      - airflow-postgres
    environment:
      - AIRFLOW_HOME=/airflow_app/airflow
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=${AIRFLOW__CORE__SQL_ALCHEMY_CONN}

```

#### Create local variables in the .env file
Host will be the container name in this case you have `airflow-postgres`
```
AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:airflow@airflow-postgres:5432/airflow
```
or to use the EXPORT these variables

```
export AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://airflow:airflow@airflow-postgres:5432/airflow

```

#### Map airflow configuration files to docker environment
place the `airflow.cfg` file into `.files` folder relative to docker-compose file and pass your custom configurations
```
volumes:
      - .files/airflow.cfg:/airflow_app/airflow/airflow.cfg
```



