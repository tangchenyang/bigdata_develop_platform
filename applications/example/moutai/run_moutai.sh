#!/bin/bash

spark-sql -f sql/build_ods_moutai.sql

spark-submit --master yarn --deploy-mode client \
             --driver-memory 256m \
             --num-executors 2 \
             --executor-memory 256m \
             --executor-cores 2 \
             --class org.example.moutai.dw.fact.DwFactMoutai