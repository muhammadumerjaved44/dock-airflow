# -*- coding: utf-8 -*-

from airflow import DAG
from airflow.operators import BashOperator,PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import os

seven_days_ago = datetime.combine(datetime.today() - timedelta(7),
                                  datetime.min.time())
now = datetime.now()
now_plus_10 = datetime.now() - timedelta(minutes=15)

min_10 = days_ago(1, minute=10)
dir_path = os.path.abspath(os.path.dirname(__file__))
parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
#parent_path_1 = os.path.abspath(os.path.join(parent_path, os.pardir))
file_path = parent_path+'/'+'main.py'
print(file_path)

def print_context(ds, **kwargs):
#    pprint(kwargs)
    print(ds)
    return ds


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': min_10,
    'email': ['muhammadumerjaved44@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
  }


dag = DAG('scrape_cdc', default_args=default_args)

run_this = PythonOperator(
    task_id='print_the_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag)

t1 = BashOperator(
task_id='testairflow',
bash_command=f'python {file_path}',
dag=dag)

t1.set_downstream(run_this)

if __name__ == "__main__":
    dag.cli()