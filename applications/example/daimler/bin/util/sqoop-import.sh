#!/bin/bash

connect=$1
username=$2
password=$3

query="$4"

targetDatabase=$5
targetTable=$6
hiveWarehouse=/user/hive/warehouse/

sqoop import \
  --connect $connect \
  --username $username \
  --password password \
  --query "$query" \
  --hive-import \
  --hive-overwrite \
  --target-dir $hiveWarehouse/$targetDatabase.db/$targetTable \
  --hive-database $targetDatabase \
  --hive-table $targetTable \
  -m 1
