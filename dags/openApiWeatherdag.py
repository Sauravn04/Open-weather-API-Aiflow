from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta, datetime
from airflow.hooks.base_hook import BaseHook
from airflow.utils.dates import days_ago

import configparser
import os, sys

path = os.environ["AIRFLOW_HOME"]

from src.utilites.upload_to_s3 import upload_file_to_s3

print("airflow_path***********", path)


args = {
    "owner": "saurav",
    "start_date": days_ago(1),  # make start date in the past
    "email": ["nayaksaurav99@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

# Define file_path, bucket_name, and s3_key
file_path = f"{path}/dags/src/output/finalOpenWeatherData.csv"
bucket_name = "saurav-weather-data"  # Replace with your S3 bucket name
s3_key = "weather-data/finalOpenWeatherData.csv"

dag = DAG(
    dag_id="openApiWeatherdag",
    default_args=args,
    schedule_interval="30 21 * * *",  # every day 21:30 HH:MM
)

t1 = BashOperator(
    task_id="start",
    bash_command='echo "***************  code start   **************"',
    dag=dag,
)

t2 = BashOperator(
    task_id="get_weather_api_code",
    bash_command=f"python {path}/dags/src/openApiWeather.py",
    dag=dag,
)

t3 = BashOperator(
    task_id="end",
    bash_command='echo "***************  code end   **************"',
    dag=dag,
)

upload_to_s3_task = PythonOperator(
    task_id="upload_to_s3",
    python_callable=upload_file_to_s3,
    op_args=[file_path, bucket_name, s3_key],
    dag=dag,
)

t1 >> t2 >> t3 >> upload_to_s3_task
