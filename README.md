# Easy way to install Apache Airflow

This image is bases on the linux debian latest and pull from the `continuumio/miniconda3`, heaving the Install the conda enviorment as `(base)`. This image also using the postgress database that helps to use run the air-flow services

## How to make the docker-compose file from this image

### Install the postgress db
Create a service for the postgres sql pull from the image `postgres:10.1-alpine`.

#### paste in docker-compose file
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

#### To presist the data we can use volumes like this
```
-volumes:
    ./postgres_data/:/var/lib/postgresql/data:rw
```

