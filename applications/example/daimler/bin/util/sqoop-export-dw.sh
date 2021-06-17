#!/bin/bash
# echo [Usage] bash sqoop-import-daimler.sh query targetDatabase targetTable
current_dir=$(cd `dirname $0` && pwd)
cd $current_dir

connect=jdbc:mysql://localhost:3306/dw
username=root
password=123456

hiveDatabase=$1
hiveTable=$2

targetDatabase=$3
targetTable=$4

bash ./sqoop-export.sh $connect $username $password $hiveDatabase $hiveTable $targetDatabase $targetTable
