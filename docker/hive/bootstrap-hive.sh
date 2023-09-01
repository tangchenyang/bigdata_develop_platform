#!/bin/bash
bash /root/software/bootstrap.sh

service mysql start

schematool -initSchema -dbType mysql --verbose

hive --service metastore &
hiveserver2 &

if [[ $1 == "-d" ]]; then
  while true; do sleep 1000; done
fi
