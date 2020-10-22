#!/bin/bash

base_path=$(cd $(dirname $0) && pwd)
cd $base_path
bash install_java.sh
bash install_hadoop.sh
bash install_mysql.sh
bash install_hive.sh
bash install_scala.sh
bash install_spark.sh
bash install_flink.sh
