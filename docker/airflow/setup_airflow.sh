#!/bin/bash
echo "setup airflow ... start "
service postgresql start

rm -f /usr/local/lib/python3.10/dist-packages/airflow/example_dags/example*.py
rm -f /usr/local/lib/python3.10/dist-packages/airflow/example_dags/tutorial*.py

airflow db init
# set config
sed -i "s/authenticate = True/authenticate = False/g" ${AIRFLOW_HOME}/airflow.cfg
sed -i "s#sql_alchemy_conn = sqlite:////root/airflow/airflow.db#sql_alchemy_conn = postgresql://airflow:airflow@localhost/airflow#g" ${AIRFLOW_HOME}/airflow.cfg
airflow db init
airflow users delete --username admin
airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email admin

#airflow standalone &
sleep 10

echo "setup airflow ... end "
