#!/bin/bash
# start ssh
/etc/init.d/ssh start &

# start Hadoop
start-all.sh

# start MySQL
service mysql start

# start Hive Server
schematool -initSchema -dbType mysql --verbose
hive --service metastore &
hiveserver2 &

# start spark connect
start-connect-server.sh --master yarn --deploy-mode client --packages org.apache.spark:spark-connect_2.12:3.5.5

if [[ $1 == "-d" ]]; then
  while true; do sleep 1000; done
fi
