import sys
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime


sys.path.append(os.path.join(os.path.dirname(__file__), 'python_scripts'))
from train_model import process_iris_data
from dbt_operator import DbtOperator

DBT_PROJECT_DIR = "/opt/airflow/dags/dbt/homework"
DBT_PROFILE = "homework"

default_args = {
    'owner': 'airflow',
    'email': ['your_email@example.com'],
    'email_on_failure': False,
    'retries': 1,
}

with DAG(
    'process_iris',
    default_args=default_args,
    start_date=datetime(2025, 4, 22),
    end_date=datetime(2025, 4, 25),
    schedule_interval='0 1 * * *',
    catchup=True,
    tags=['homework', 'ml'],
) as dag:


    dbt_args = {
        'profile': DBT_PROFILE,
        'project_dir': DBT_PROJECT_DIR,
        'env_vars': {'DBT_PROFILES_DIR': '/opt/airflow/dags/dbt'}

    }


    dbt_deps = DbtOperator(task_id='dbt_deps', command='deps', **dbt_args)
    dbt_seed = DbtOperator(task_id='dbt_seed', command='seed', **dbt_args)
    dbt_run = DbtOperator(
        task_id='dbt_run',
        command='run',
        select=['+iris_processed'],
        vars={'execution_date': '{{ ds }}'},
        **dbt_args
    )


    train_ml = PythonOperator(
        task_id='train_model',
        python_callable=process_iris_data,
        provide_context=True,
    )


    send_email = EmailOperator(
        task_id='send_success_email',
        to='oriekhovkyrylo@meta.ua',
        subject='Airflow: Iris Pipeline Success ({{ ds }})',
        html_content='<p>ML Pipeline completed successfully for {{ ds }}</p>'
    )


    dbt_deps >> dbt_seed >> dbt_run >> train_ml >> send_email
