import boto3
from dotenv import dotenv_values 
from logger.Logger import Log
from pathlib import Path
import os
from datetime import datetime,timezone
import time
from multiprocessing.pool import ThreadPool 
from pathlib import Path

# putting raw file into s3 
log = Log(__name__)

config = dotenv_values(os.path.join(Path(__file__).parent,"environment.env"))

client = boto3.client(
            service_name='s3',
            region_name=config['region'],
            aws_access_key_id=config['access_key'],
            aws_secret_access_key=config['secret_key']
        )

def uploadig_file(myfile):
    log.logger.info(f'now putting {myfile} to raw_zone')
    client.upload_file(myfile,config['bucket'],f'{Path(myfile).stem}_{datetime.now()}.json')
    log.logger.info(f'successfully putting {myfile} to raw_zone')

start = time.perf_counter()
log.logger.info("now putting raw file to s3")

raw_json = list(Path(__file__).parents[1].joinpath('zone1').glob('*.json'))
raw_str_json = list(map(lambda x: str(x),raw_json))
pool = ThreadPool(processes=len(raw_str_json)*2) 
pool.map(uploadig_file, raw_str_json) 



end = time.perf_counter()
log.logger.info("successfully put raw file to s3")
log.logger.info(f"put raw file to s3 have used {end - start}s")
