FROM apache/airflow:latest

USER root 
RUN apt update && \
    apt-get install -y vim && \ 
    apt-get install -y libpq-dev gcc && \ 
    apt-get clean;

USER airflow 

COPY requirement.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt && \
    pip uninstall psycopg2 -y && \ 
    pip install psycopg2 
EXPOSE 3000