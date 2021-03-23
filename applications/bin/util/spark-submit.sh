# 提交 spark 任务
spark-submit --master yarn --deploy-mode client \
             --driver-memory 256m \
             --num-executors 2 \
             --executor-memory 256m \
             --executor-cores 2 \
             --class $@