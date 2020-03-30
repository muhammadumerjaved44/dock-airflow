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

### Step 2: Initialize the database for the Airflow
Apache require to run the migrations in the postgres database so that Airflow has to run the command `airflow initdb`. For this you have to create the separate service

#### airflow initdb
```
 #  airflow initdb service configuration #1
  airflow-initdb:
    container_name: airflow-initdb
    # build: .
    image: muhammadumerjaved44/dock-airflow
    entrypoint: airflow initdb
    depends_on:
      - airflow-postgres
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
      - AIRFLOW_HOME=/airflow_app/airflow
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=${AIRFLOW__CORE__SQL_ALCHEMY_CONN}
    volumes:
      - ./dags:/airflow_app/dags
      - .files/airflow.cfg:/airflow_app/airflow/airflow.cfg
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
place the `airflow.cfg` file into `.files` folder relative to docker-compose file and pass your custom configurations. make the `dag` folder relative to the docker-compose file so that you can have relative task here in the dag folder and map to the dockers `dag` folder
```
    volumes:
      - ./dags:/airflow_app/dags
      - .files/airflow.cfg:/airflow_app/airflow/airflow.cfg
```

### Step 3: Run the Server for the Airflow

#### airflow webserver
```
airflow-python:
    container_name: airflow-python
    image: muhammadumerjaved44/dock-airflow
    stdin_open: true
    privileged: true
    tty: true
    restart: always
    entrypoint: airflow webserver -p 8080
    ports:
      - "7053:8080"
    depends_on:
      - airflow-initdb
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
      - CURRENT_DIR=/airflow_app
      - AIRFLOW_HOME=/airflow_app/airflow
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=${AIRFLOW__CORE__SQL_ALCHEMY_CONN}
    volumes:
      - .files/airflow.cfg:/airflow_app/airflow/airflow.cfg
      - ./dags:/airflow_app/dags
    healthcheck:
      test: ["CMD-SHELL", "[ -f /airflow_app/airflow/airflow-webserver.pid ]"]
      interval: 30s
      timeout: 30s
      retries: 3
```

### Step 4: Run the Scheduler for the Airflow

#### airflow scheduler
```
airflow-scheduler:
    # build: .
    image: muhammadumerjaved44/dock-airflow
    container_name: airflow-scheduler
    depends_on:
      - airflow-python
    volumes:
      - .files/airflow.cfg:/airflow_app/airflow/airflow.cfg
      - ./dags:/airflow_app/dags
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
      - AIRFLOW_HOME=/airflow_app/airflow
      - AIRFLOW__CORE__SQL_ALCHEMY_CONN=${AIRFLOW__CORE__SQL_ALCHEMY_CONN}
    entrypoint: airflow scheduler
    stdin_open: true
    privileged: true
    tty: true
    healthcheck:
      test: ["CMD-SHELL", "[ -f /airflow_app/airflow/airflow-scheduler.pid ]"]
      interval: 30s
      timeout: 30s
      retries: 3
```




