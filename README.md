# 安装伪分布式Hadoop集群
## 手动安装
参考 [docs/Manual-Install-Hadoop.md](https://github.com/tangchenyang/bigdata_develop_platform/blob/master/docs/Manual-Install-Hadoop.md)
## DockerFile 安装
### build image
```shell
cd docker/hadoop
docker build . -t hdp:v0.1
```
### run container
```shell
docker run -itd --privileged --name hadoop -p 9870:9870 -p 8088:8088 -p 4040:4040 -p 3307:3306 hdp:v0.1
```
### HDFS WEB UI
[http://localhost:9870](http://localhost:9870/)

### YARN WEB UI
[http://localhost:8088](http://localhost:8088/)

## CLi Command Example
### 进入容器
```shell
docker exec -it hadoop bash
```
### HDFS 命令 Example
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

### MapReduce Job Example 
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

### YARN 命令 Example 
```shell
# RUNNING 时
yarn application --list
# KILL RUNNING App
yarn application --kill <application_id>
# FINISHED 时
yarn application --list --appStates ALL
```
