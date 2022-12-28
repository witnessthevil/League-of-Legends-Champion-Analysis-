import os
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
from datetime import datetime
from dotenv import dotenv_values
from pathlib import Path
import time
from logger.Logger import Log
import pandera as pa
from dagster import *

################################################################################################
# This task we will be using pandas, dagster and pandera for data cleansing and data validation#
################################################################################################
log = Log(__name__)

@op
def read_json() -> DataFrame:
    df = pd.read_json("/opt/airflow/zone1/lol_counter_stat.json",lines=True)
    return df

@op
def data_validation(df:DataFrame) -> DataFrame:
    schema2 = pa.DataFrameSchema(
        {
            "Champ_Name":pa.Column(str,nullable=False),
            "champ_counter":pa.Column("object",nullable=False
            ,checks=[
                pa.Check(lambda x: x.explode().dtypes == "object"),
            ]),
            "countered_by":pa.Column("object",nullable=False,checks=[
                pa.Check(lambda x: x.explode().dtypes == "object"),
            ])
        }
    )
    validated_df = schema2.validate(df)
    return validated_df

@op
def data_cleansing(df:DataFrame) -> DataFrame:
    new_df = df.assign(win_rate = lambda x: x["champ_counter"] + x["countered_by"])\
           .explode('win_rate')

    new_df['win_per'] = new_df['win_rate'].apply(lambda x: x[1])
    new_df['champ'] = new_df['win_rate'].apply(lambda x: x[0])
    new_df = new_df.drop(['champ_counter','countered_by','win_rate'],axis=1)
    new_df["date"] = str(datetime.date(datetime.today()))
    new_df = new_df.rename(columns={'champ':'opp_champ',"Champ_Name":"champ"})
    return new_df
@op
def df_to_pg(df:DataFrame):
    config = dotenv_values(os.path.join(Path(__file__).parent,"environment.env"))

    user = config["pg_name"]
    password = config["pg_password"]
    database = config["pg_database"]

    pg_engine = create_engine(f"postgresql+psycopg2://{user}:{password}@host.docker.internal:5432/{database}")
    df.to_sql('lol_counter_stat',pg_engine,if_exists='append',index=False)

@op
def df_to_file(df:DataFrame):
    df.to_json("/opt/airflow/processed_zone/lol_clean_counter_stat.json",orient='records',lines=True)

@job
def counter_stat_job():
    raw_df = read_json()
    clean_df = data_cleansing(raw_df)
    df_to_pg(clean_df)
    df_to_file(clean_df)

if __name__ == "__main__":
    start = time.perf_counter()
    result = counter_stat_job.execute_in_process()
    end = time.perf_counter()
    log.logger.info("successfully put lol_basic_stat to pg and redshift")
    log.logger.info(f"put lol_basic_stat to pg and file have used {end - start}s")