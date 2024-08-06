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

if [[ $1 == "-d" ]]; then
  while true; do sleep 1000; done
fi
