#!/bin/bash

$APPLICATIONS_HOME/bin/util/spark-sql-f.sh sql/build_ods_moutai.sql

$APPLICATIONS_HOME/bin/util/spark-submit.sh org.example.moutai.dw.fact.DwFactMoutai jars/example-1.0-SNAPSHOT.jar
