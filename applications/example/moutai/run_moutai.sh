#!/bin/bash

spark-sql -f sql/build_ods_moutai.sql

jarPath=$APPLICATIONS_HOME/lib
spark-submit --master yarn --deploy-mode client \
             --jars $jarPath/base-1.0-SNAPSHOT.jar \
             --class org.example.moutai.dw.fact.DwFactMoutai jars/example-1.0-SNAPSHOT.jar

