# 创建容器
## 拉取ubuntu镜像，启动容器
```shell
docker pull ubuntu:latest # todo change to hive image 
```

## 启动容器
```shell
docker run -itd --privileged -p 9870:9870 -p 8088:8088 -p 4040:4040 -p 10000:10000 --name hive-spark hive:v0.1
```

## 进入容器
```shell
docker exec -it hive-spark bash
```
以下操作均在容器内部
# 安装 Scala 
## 下载安装包
```shell
wget https://downloads.lightbend.com/scala/2.12.19/scala-2.12.19.tgz -P /root/install_packages/
```

## 解压
```shell
tar -zxvf /root/install_packages/scala-2.12.19.tgz -C /root/software/
```

## 配置环境变量
```shell
echo "" >> /etc/profile
echo "# scala" >> /etc/profile
echo "export SCALA_HOME=/root/software/scala-2.12.19" >> /etc/profile
echo "export PATH=\$PATH:\$SCALA_HOME/bin" >> /etc/profile
```

## 加载环境变量
```shell
source /etc/profile
```

# 安装 Spark
## 下载安装包
```shell
wget https://dlcdn.apache.org/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz -P /root/install_packages/
```

## 解压
```shell
tar -zxvf /root/install_packages/spark-3.5.1-bin-hadoop3.tgz  -C /root/software/
```

## 配置环境变量
```shell
echo "" >> /etc/profile
echo "# spark" >> /etc/profile
echo "export SPARK_HOME=/root/software/spark-3.5.1-bin-hadoop3" >> /etc/profile
echo "export PATH=\$PATH:\$SPARK_HOME/bin" >> /etc/profile
```

## 加载环境变量
```shell
source /etc/profile
```
## 修改配置
```shell
SPARK_CONF_DIR=${SPARK_HOME}/conf
```

### spark-env.sh
```shell
cp ${SPARK_CONF_DIR}/spark-env.sh.template ${SPARK_CONF_DIR}/spark-env.sh
echo "export JAVA_HOME=${JAVA_HOME}" >> ${SPARK_CONF_DIR}/spark-env.sh
echo "export SCALA_HOME=${SCALA_HOME}" >> ${SPARK_CONF_DIR}/spark-env.sh
echo "export HADOOP_HOME=${HADOOP_HOME}" >> ${SPARK_CONF_DIR}/spark-env.sh
echo "export HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop" >> ${SPARK_CONF_DIR}/spark-env.sh
echo "export SPARK_HOME=${SPARK_HOME}" >> ${SPARK_CONF_DIR}/spark-env.sh
```
### hive-site.xml
```shell
cat << EOF >> ${SPARK_CONF_DIR}/hive-site.xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>hive.metastore.uris</name>
    <value>thrift://localhost:9083</value>
    <description>Thrift URI for the remote metastore. Used by metastore client to connect to remote metastore.</description>
  </property>
  <property>
    <name>hive.metastore.warehouse.dir</name>
    <value>/user/hive/warehouse</value>
    <description>location of default database for the warehouse</description>
  </property>
</configuration>
EOF
```

## 运行 Example 
```shell
spark-submit \
  --class org.apache.spark.examples.SparkPi \
  --master yarn \
  --deploy-mode client \
  ${SPARK_HOME}/examples/jars/spark-examples_2.12-3.5.1.jar \
  1000
```

