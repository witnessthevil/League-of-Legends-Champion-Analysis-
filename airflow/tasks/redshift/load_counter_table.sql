COPY lol_counter_stat
FROM 's3://{bucket_name}/lol_clean_counter_stat_{date}.json' 
with credentials as 'aws_access_key_id={aws_access_id};aws_secret_access_key={aws_secret_key}' 
json 'auto'
DATEFORMAT AS 'MM/DD/YYYY';