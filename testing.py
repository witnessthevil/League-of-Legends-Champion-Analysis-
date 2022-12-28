from pyspark.sql import SparkSession 
import pandas as pd
import pandera as pa
from itertools import pairwise


#df = pd.read_json("/Users/danie/new_project_lol_stat/airflow/zone1/lol_basic_stat.json",lines=True)
df2 = pd.read_json("/Users/danie/new_project_lol_stat/airflow/zone1/lol_counter_stat.json",lines=True)
print(df2.info())
#schema = pa.DataFrameSchema(
#        {
#            "name":pa.Column(str,nullable=False),
#            "role":pa.Column(str,checks=pa.Check.str_contains("ADC|SUPPORT|JUNGLE|MID|TOP")),
#            "tier":pa.Column(str),
#            "score":pa.Column(float,nullable=False,checks=pa.Check(lambda x: x.between(0,100))),
#            "trend":pa.Column(float,nullable=True,checks=pa.Check(lambda x: x.between(-100,100))),
#            "win_rate":pa.Column(str,nullable=False,checks=pa.Check(lambda x: x.str[:-1].astype(float).between(0,100))),
#            "role_per":pa.Column(str,nullable=False,checks=pa.Check(lambda x: x.str[:-1].astype(float).between(0,100))),
#            "pick_per":pa.Column(str,nullable=False,checks=pa.Check(lambda x: x.str[:-1].astype(float).between(0,100))),
#            "ban_per":pa.Column(str,nullable=False,checks=pa.Check(lambda x: x.str[:-1].astype(float).between(0,100))),
#            "kda":pa.Column(float,nullable=False,checks=pa.Check(lambda x: x.between(0,10))),
#        }
#    )
#result = schema.validate(df,lazy=True)


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
result2 = schema2.validate(df2,lazy=True)
print(result2)

new_df = df2['champ_counter']
df2 = new_df.explode().explode().reset_index(drop=True)
print(df2)