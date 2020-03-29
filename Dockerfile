FROM continuumio/miniconda3

# activate conda enviorment
RUN /bin/sh -c conda activate base
ENV CURRENT_DIR /airflow_app
WORKDIR /${CURRENT_DIR}
# COPY requirements.txt .
# RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    devscripts \
    equivs \
    git-buildpackage \
    git \
    lsb-release \
    make \
    openssh-client \
    pristine-tar \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4

ENV AIRFLOW_HOME=/${CURRENT_DIR}/airflow
RUN pip install apache-airflow
RUN conda install -c bioconda mysqlclient
RUN pip install psycopg2-binary
RUN conda install -c conda-forge pymysql
RUN pip install 'apache-airflow[mysql,postgres,gcp]'


ENV CONDA_PACKAGES="\
    anaconda::pyodbc"

RUN conda install $CONDA_PACKAGES


COPY . /${CURRENT_DIR}