FROM apache/airflow:2.4.3-python3.10
#USER root
COPY python_scripts/*  /opt/airflow/python_scripts/
COPY dags/*   /opt/airflow/dags/
COPY requirements.txt /
#USER airflow 
RUN pip install --no-cache-dir -r /requirements.txt
#EXPOSE 8080
#CMD["airflow","standalone"]
