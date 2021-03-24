#!/bin/bash
# 提交 spark 任务

# concat jars
for jar in $(ls $APPLICATIONS_HOME/lib)
do
    jars="$jars$APPLICATIONS_HOME/lib/$jar,"
done

spark-submit --master yarn --deploy-mode client \
             --jars $jars \
             --class $@
