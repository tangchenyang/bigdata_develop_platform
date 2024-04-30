#!/bin/bash
# start postgres
service postgresql start

# start airflow
airflow standalone &

if [[ $1 == "-d" ]]; then
  while true; do sleep 1000; done
fi
