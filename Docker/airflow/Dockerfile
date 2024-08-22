FROM apache/airflow:2.10.0
RUN pip install --upgrade setuptools pip wheel
COPY ./airflow/requirements.txt .
RUN pip install -r requirements.txt
USER root
RUN apt-get update
RUN apt-get install wget
