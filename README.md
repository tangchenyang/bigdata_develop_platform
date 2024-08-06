# 安装 Spark 集群
## 安装集群 
参考 [Manual-Install-Spark.md](docs/Manual-Install-Spark.md)
## 验证服务
### HDFS
#### HDFS WEB UI
[http://localhost:9870](http://localhost:9870/)
#### HDFS 命令 Example
```shell
# list folders/files
hdfs dfs -ls /
# put file
hdfs dfs -put /root/software/hadoop-3.3.5/README.txt /
# list folders/files
hdfs dfs -ls /
# get file
cd ~
hdfs dfs -get /README.txt .
ls .
```

### MapReduce
#### MapReduce Job Example
[WordCount 源码](https://github.com/apache/hadoop/blob/trunk/hadoop-mapreduce-project/hadoop-mapreduce-examples/src/main/java/org/apache/hadoop/examples/WordCount.java)
```shell

# 上传测试文件
hdfs dfs -mkdir /input
hdfs dfs -put /root/software/hadoop-3.3.5/README.txt /input/
hdfs dfs -ls /input

# 运行WordCount
hadoop jar ${HADOOP_HOME}/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.5.jar wordcount /input/ /output

# 查看输出
hdfs dfs -ls /output
hdfs dfs -cat /output/part-r-00000
```

### YARN
#### YARN WEB UI
[http://localhost:8088](http://localhost:8088/)

#### YARN 命令 Example
```shell
# RUNNING 时
yarn application --list
# KILL RUNNING App
yarn application --kill <application_id>
# FINISHED 时
yarn application --list --appStates ALL
```

### Hive
#### Hive 命令 Example
```shell
hive -e "CREATE database test_db";
hive -e "SHOW DATABASES";
```
### Spark
#### Spark Job Example 
```shell
spark-submit \
  --class org.apache.spark.examples.SparkPi \
  --master yarn \
  --deploy-mode client \
  ${SPARK_HOME}/examples/jars/spark-examples_2.12-3.5.1.jar \
  1000
```
