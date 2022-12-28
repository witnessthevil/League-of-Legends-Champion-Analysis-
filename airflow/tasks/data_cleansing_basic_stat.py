import pandas as pd
from pandas import DataFrame
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import dotenv_values
import os
from pathlib import Path
from logger.Logger import Log
import time
from dagster import *
import pandera as pa


log = Log(__name__)

################################################################################################
# This task we will be using pandas, dagster and pandera for data cleansing and data validation#
################################################################################################

@op
def reading_json() -> DataFrame:
    df = pd.read_json("/opt/airflow/zone1/lol_basic_stat.json",lines=True)
    return df

# data validation on columns'datatype and completeness
@op
def data_validation(df:DataFrame) -> DataFrame:
    schema = pa.DataFrameSchema(
        {
            "champ":pa.Column(str,nullable=False),
            "role":pa.Column(str,checks=pa.Check.str_contains("ADC|SUPPORT|JUNGLE|MID|TOP")),
            "tier":pa.Column(str),
            "score":pa.Column(float,nullable=False,checks=pa.Check(lambda x: x.between(0,100))),
            "trend":pa.Column(float,nullable=True,checks=pa.Check(lambda x: x.between(-100,100))),
            "win_rate":pa.Column(str,nullable=False,checks=pa.Check(lambda x: x.str[:-1].astype(float).between(0,100))),
            "role_per":pa.Column(str,nullable=False,checks=pa.Check(lambda x: x.str[:-1].astype(float).between(0,100))),
            "pick_per":pa.Column(str,nullable=False,checks=pa.Check(lambda x: x.str[:-1].astype(float).between(0,100))),
            "ban_per":pa.Column(str,nullable=False,checks=pa.Check(lambda x: x.str[:-1].astype(float).between(0,100))),
            "kda":pa.Column(float,nullable=False,checks=pa.Check(lambda x: x.between(0,10))),
        }
    )
    result = schema.validate(df,lazy=True)
    return result

# replace the trend as na 
@op
def data_cleaning(df:DataFrame) -> DataFrame:
    log.logger.info('now perform data cleansing on lol_basic_stat')
    # removing the null
    df = df.fillna(0)
    # remove the percentage
    df["win_rate"] = df["win_rate"].str[:-1]
    df["role_per"] = df["role_per"].str[:-1]
    df["pick_per"] = df["pick_per"].str[:-1]
    df["ban_per"] = df["ban_per"].str[:-1]
    df["tier"] = df["tier"].str[-2:].replace(" ",'')

    # changing 4 columns' datatype to float
    df= df.astype({'win_rate':float,"role_per":float,"pick_per":float,"ban_per":float})

    # adding date
    df["date"] = str(datetime.date(datetime.today()))
    #df['date'] = datetime.today().strftime('%Y-%m-%d')
    log.logger.info('successfully perform data cleansing on lol_basic_stat')
    log.logger.info('Now putting dataframe into pg and redshift')
    return df

@op
def sending_to_pg(df:DataFrame):

    config = dotenv_values(os.path.join(Path(__file__).parent,"environment.env"))
    user = config["pg_name"]
    password = config["pg_password"]
    database = config["pg_database"]

    pg_engine = create_engine(f"postgresql+psycopg2://{user}:{password}@host.docker.internal:5432/{database}")
    df.to_sql('lol_basic_stat',con=pg_engine,if_exists="append",index=False)

    log.logger.info("successfully put lol_basic_stat to pg and redshift")

@op
def df_to_file(df:DataFrame):
    df.to_json("/opt/airflow/processed_zone/lol_clean_basic_stat.json",orient='records',lines=True)

@job
def data_cleansing_whole_job():
    raw_df = reading_json()
    validated_df = data_validation(raw_df)
    clean_df = data_cleaning(validated_df)
    sending_to_pg(clean_df)
    df_to_file(clean_df)

if __name__ == "__main__":
    start = time.perf_counter()
    result = data_cleansing_whole_job.execute_in_process()
    end = time.perf_counter()
    log.logger.info(f"put lol_basic_stat to pg and redshift have used {end - start}s")


# then add the validation part