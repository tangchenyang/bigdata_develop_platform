#!/bin/bash
connect=$1
username=$2
password=$3

hiveDatabase=$4
hiveTable=$5

targetDatabase=$6
targetTable=$7
hiveWarehouse=/user/hive/warehouse/

sqoop export \
  --connect $connect \
  --username $username \
  --password password \
  --export-dir $hiveWarehouse/${hiveDatabase}.db/$hiveTable \
  --table $targetDatabase.$targetTable \
  -m 1
