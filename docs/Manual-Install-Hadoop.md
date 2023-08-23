# 创建容器
## 拉取ubuntu镜像，启动容器
```shell
docker pull ubuntu:latest
```

## 启动容器
```shell
docker run -itd --privileged -p 9000:9000 -p 50070:50070 -p 9870:9870 -p 8088:8088 -p 4040:4040 -p 3306:3306 --name hadoop ubuntu:latest
```

## 进入容器
```shell
docker exec -it hadoop bash
```
以下操作均在容器内部

# 配置 SSH 免密
## 安装SSH服务
```shell
apt update
apt install -y vim openssh-server 
/etc/init.d/ssh start
```

## ssh 免密 
```shell
ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa -q
cat ~/.ssh/*.pub > ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
sed -i "s/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/g" /etc/ssh/ssh_config  
```

# 安装软件
## 创建用于存放安装包和软件的目录
```shell
mkdir -p /root/software
mkdir -p /root/install_packages
```

## 安装 JDK 
### apt 安装 jdk8
```shell
apt install -y openjdk-8-jdk
```

### 配置 JAVA_HOME 
```shell
echo "" >> /etc/profile
echo "# java" >> /etc/profile
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64/" >> /etc/profile
echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> /etc/profile
```

## 安装 Hadoop
### 下载 Hadoop 安装包 
```shell
wget https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.3.5/hadoop-3.3.5.tar.gz -P /root/install_packages/
# 下载较慢，可以使用已下载的本地tar包
# docker cp ./hadoop-3.3.5.tar.gz hadoop://root/install_packages/
```

### 解压
```shell
tar -zxvf /root/install_packages/hadoop-3.3.5.tar.gz -C /root/software/
```

### 配置环境变量
```shell
echo "" >> /etc/profile
echo "# hadoop" >> /etc/profile
echo "export HADOOP_HOME=/root/software/hadoop-3.3.5" >> /etc/profile
echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin" >> /etc/profile
```
### 加载环境变量
```shell
source /etc/profile
```

# 配置 Hadoop 
## 创建 dfs 目录
- name: NameNode dir
- data: DataNode dir
```shell
mkdir -p ${HADOOP_HOME}/dfs/name
mkdir -p ${HADOOP_HOME}/dfs/data
```
## 修改 core-site.xml
```shell
sed -i "/configuration/d" ${HADOOP_HOME}/etc/hadoop/core-site.xml
cat << EOF >> ${HADOOP_HOME}/etc/hadoop/core-site.xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
EOF
```
## 修改 hdfs-site.xml
```shell
sed -i "/configuration/d" ${HADOOP_HOME}/etc/hadoop/hdfs-site.xml
cat << EOF >> ${HADOOP_HOME}/etc/hadoop/hdfs-site.xml
<configuration>
    <property>
            <name>dfs.namenode.name.dir</name>
            <value>file:${HADOOP_HOME}/dfs/name</value>
    </property>
    <property>
            <name>dfs.datanode.data.dir</name>
            <value>file:${HADOOP_HOME}/dfs/data</value>
    </property>
</configuration>
EOF
```
## 修改 yarn-site.xml
```shell
sed -i "/configuration/d" ${HADOOP_HOME}/etc/hadoop/yarn-site.xml
cat << EOF >> ${HADOOP_HOME}/etc/hadoop/yarn-site.xml
<configuration>
    <property>
        <name>yarn.resourcemanager.address</name>
        <value>localhost:8032</value>
    </property>
    <property>
        <name>yarn.resourcemanager.scheduler.address</name>
        <value>localhost:8030</value>
    </property>
    <property>
        <name>yarn.resourcemanager.resource-tracker.address</name>
        <value>localhost:8031</value>
    </property>
    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
    <property>
        <name>yarn.nodemanager.env-whitelist</name>
        <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value>
    </property>
</configuration>
EOF
```

## 修改 mapred-site.xml
```shell
sed -i "/configuration/d" ${HADOOP_HOME}/etc/hadoop/mapred-site.xml
cat << EOF >> ${HADOOP_HOME}/etc/hadoop/mapred-site.xml
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>yarn.app.mapreduce.am.env</name>
        <value>HADOOP_MAPRED_HOME=/root/software/hadoop-3.3.5</value>
    </property>
    <property>
        <name>mapreduce.map.env</name>
        <value>HADOOP_MAPRED_HOME=/root/software/hadoop-3.3.5</value>
    </property>
    <property>
        <name>mapreduce.reduce.env</name>
        <value>HADOOP_MAPRED_HOME=/root/software/hadoop-3.3.5</value>
    </property>
    <property>
        <name>mapreduce.application.classpath</name>
        <value>/root/software/hadoop-3.3.5/share/hadoop/mapreduce/*:/root/software/hadoop-3.3.5/share/hadoop/mapreduce/lib/*</value>
    </property>
</configuration>
EOF
```

## 修改 hadoop-env.sh
```shell
sed -i "s/# export HDFS_NAMENODE_USER=hdfs/export HDFS_NAMENODE_USER=root\nexport HDFS_DATANODE_USER=root\nexport HDFS_SECONDARYNAMENODE_USER=root\nexport YARN_NODEMANAGER_USER=root\nexport YARN_RESOURCEMANAGER_USER=root\n/g" ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh
sed -i "s?# export JAVA_HOME=?export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64?g" ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh
```


## 格式化 hdfs
有 has been successfully formatted 即为成功
```shell
hdfs namenode -format
```
# 启动 Hadoop
## 启动 HDFS 
```shell
start-dfs.sh
```
## 访问 HDFS WEB UI
[http://localhost:9870](http://localhost:9870/)


## 启动 YARN 
```shell
start-yarn.sh
```
## 访问 YARN WEB UI
[http://localhost:8088](http://localhost:8088/)

