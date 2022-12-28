from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
#engine = create_engine("redshift+psycopg2://witnessthevil:Uttalogical00!@tf-daniel-clustering.cqq8hx1h9dt9.us-east-1.redshift.amazonaws.com:5439/lol_stat2")
#
#df = pd.read_sql("select * from lol_basic_stat",engine)
#print(df)

print(datetime.today().strftime('%Y-%m-%d'))