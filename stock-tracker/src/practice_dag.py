from airflow import DAG
import stock

from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'email': ['airflow@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
}

# [START instantiate_dag]
with DAG(
    'practice_etl_dag',
    default_args=default_args,
    description='ETL DAG stock-tracker',
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['practice'],
) as dag:
    def portfolio_update(portfolio, **kwargs):
        for ticker in portfolio:
            pass
            #stock.stock(f"{ticker}"})
        