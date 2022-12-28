from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow_dbt.operators.dbt_operator import DbtRunOperator

schedule_interval = "0 10 * * *"
start_date = days_ago(1)
default_args = {"owner": "airflow", "depends_on_past": False}

with DAG(
    dag_id="Can_I_change_name_to_this",
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1,
) as dag:

    scrape_basic = BashOperator(
        task_id = 'scrape_basic',
        bash_command = 'python /opt/airflow/tasks/lol_champ_basic_stat.py '
    )
    scrape_counter = BashOperator(
        task_id = 'scrape_counter',
        bash_command = 'python /opt/airflow/tasks/lol_champ_counter_stat.py '
    )
    task_3 = BashOperator(
        task_id = 'task_3',
        bash_command = 'sleep 1'
    )
    put_raw_to_s3 = BashOperator(
        task_id = 'put_raw_to_s3',
        bash_command = 'python /opt/airflow/tasks/raw_put_to_s3.py '
    )
    basic_data_cleansing = BashOperator(
        task_id = 'basic_data_cleansing',
        bash_command = 'python /opt/airflow/tasks/data_cleansing_basic_stat.py'
    )
    counter_data_cleansing = BashOperator(
        task_id = 'counter_data_cleansing',
        bash_command = 'python /opt/airflow/tasks/data_cleansing_counter_stat.py'
    )
    processed_put_to_s3 = BashOperator(
        task_id = 'processed_put_to_s3',
        bash_command = 'python /opt/airflow/tasks/processed_put_to_s3.py'
    )

    remove_raw = BashOperator(
        task_id = 'remove_raw',
        bash_command = 'rm -f /opt/airflow/zone1/*'
    )

    sleep_task = BashOperator(
        task_id = 'task_10',
        bash_command = 'sleep 1'
    )

    remove_processed = BashOperator(
        task_id = 'remove_processed',
        bash_command = 'rm -f /opt/airflow/processed_zone/*'
    )

    sleep_task2 = BashOperator(
        task_id = 'task_15',
        bash_command = 'sleep 1'
    )

    load_basic_to_pg = BashOperator(
        task_id = 'load_basic_to_pg',
        bash_command = 'python /opt/airflow/tasks/redshift/basic_load_to_redshift.py'
    )
    load_counter_to_pg = BashOperator(
        task_id = 'load_counter_to_pg',
        bash_command = 'python /opt/airflow/tasks/redshift/counter_load_to_redshift.py'
    )
    #move_logger_to_site = BashOperator(
    #    task_id = 'move_logger_to_site',
    #    bash_command = 'cp -R /opt/airflow/tasks/logger /home/airflow/.local/lib/python3.7/site-packages'
    #)
    
    [scrape_basic,scrape_counter] >> task_3 
    task_3 >> [put_raw_to_s3,basic_data_cleansing,counter_data_cleansing]
    [put_raw_to_s3,basic_data_cleansing,counter_data_cleansing] >> sleep_task  >> [processed_put_to_s3,remove_raw]
    [processed_put_to_s3,remove_raw] >> sleep_task2 >> [load_basic_to_pg,load_counter_to_pg] >> remove_processed