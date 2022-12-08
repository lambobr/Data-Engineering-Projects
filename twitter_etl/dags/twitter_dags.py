from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from datetime import timedelta

default_args = {'owner':'airflow',
                'depends_on_past': False,
                'start_date': datetime(2020,1,1),
                'email': 'lambobr1994@gmail.com',
                'email_on_failure': False,
                'email_on_retry': False,
                'retries': 1,
                'retry_delay': timedelta(minutes=1)
                }

with DAG(dag_id='twitter_etl', default_args=default_args,schedule_interval=timedelta(hours=6) , catchup=False) as dag:

    extract = BashOperator(task_id="extract", bash_command="python3 /opt/airflow/python_scripts/extract.py")
    transform = BashOperator(task_id="transform", bash_command="python3 /opt/airflow/python_scripts/transform.py")
    load = BashOperator(task_id="load", bash_command="python3 /opt/airflow/python_scripts/load.py")
    finish = BashOperator(task_id="finish", bash_command="echo 'Twitter ETL successful'")

    extract >> transform >> load >> finish

