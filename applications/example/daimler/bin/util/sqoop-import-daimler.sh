#!/bin/bash
# echo [Usage] bash sqoop-import-daimler.sh query targetDatabase targetTable
current_dir=$(cd `dirname $0` && pwd)
cd $current_dir

connect=jdbc:mysql://localhost:3306/daimler
username=root
password=123456

query="$1"

targetDatabase=$2
targetTable=$3

bash ./sqoop-import.sh $connect $username $password $query $targetDatabase $targetTable
