from pathlib import Path
import psycopg2
from dotenv import dotenv_values
import os
from datetime import datetime
import time
import sys

#sys.path.append(Path(__file__).parents[1].joinpath)
sys.path.insert(0,"/opt/airflow/tasks")
from logger.Logger import Log
log = Log(__name__)

config=dotenv_values("/opt/airflow/tasks/environment.env")
conn = psycopg2.connect(
            host=config["host"],
            port=config["port"],
            user=config["redshift_username"],
            password=config["redshift_password"],
            dbname=config["redshift_database"],
        )
query_cursor = open(Path(__file__).parent.joinpath('load_basic_table.sql'),'r')
query = query_cursor.read().format(
    bucket_name=config["processed_bucket"],
    date=datetime.today().strftime('%Y-%m-%d'),
    aws_access_id=config["access_key"],
    aws_secret_key=config["secret_key"]
)
start  = time.perf_counter()
cursor = conn.cursor()
cursor.execute(query)
conn.commit()
cursor.close()
conn.close()
end = time.perf_counter()
log.logger.info("successfully put basic lol stat to redshift")
log.logger.info(f"put s3 basic lol stat to redshift have used {end - start}s")