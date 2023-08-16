```shell
# 宿主机
docker pull ubuntu:latest
docker run -itd --privileged -p 9000:9000 -p 50070:50070 -p 9870:9870 -p 8088:8088 -p 4040:4040 --name hadoop ubuntu:latest 
docker exec -it hadoop bash

# 容器
apt update

## install ssh
apt install -y vim openssh-server 
/etc/init.d/ssh start

## ssh 免密 
ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa -q
cat ~/.ssh/*.pub > ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
sed -i "s/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/g" /etc/ssh/ssh_config  

yum install -y net-tools telnet iptables sudo initscripts vim passwd openssh-server openssh-clients curl git 


mkdir -p /root/software
mkdir -p /root/install_packages

# 宿主机
cd /Users/chenyang.tang-fox/Workspace/docker/hadoop/install_packages
docker cp hadoop-3.3.5-aarch64.tar.gz hadoop:/root/install_packages
docker cp jdk-8u371-linux-aarch64.tar.gz hadoop:/root/install_packages
docker cp apache-hive-3.1.3-bin.tar.gz hadoop:/root/install_packages

# 容器
cd ~
tar -zxf install_packages/jdk-8u371-linux-aarch64.tar.gz -C /root/software/
tar -zxf install_packages/hadoop-3.3.5-aarch64.tar.gz -C /root/software/
tar -zxf install_packages/apache-hive-3.1.3-bin.tar.gz -C /root/software/

echo "" >> /etc/profile
echo "# java" >> /etc/profile
echo "export JAVA_HOME=/root/software/jdk1.8.0_371" >>  /etc/profile
echo "export PATH=\$PATH:\$JAVA_HOME/bin" >>  /etc/profile

echo "" >> /etc/profile
echo "# hadoop" >> /etc/profile
echo "export HADOOP_HOME=/root/software/hadoop-3.3.5" >> /etc/profile
echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin" >> /etc/profile

echo "" >> /etc/profile
echo "# hive" >> /etc/profile
echo "export HIVE_HOME=/root/software/apache-hive-3.1.3-bin" >> /etc/profile
echo "export PATH=\$PATH:\$HIVE_HOME/bin" >> /etc/profile

source /etc/profile
mkdir -p ${HADOOP_HOME}/dfs/name
mkdir -p ${HADOOP_HOME}/dfs/data

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

sed -i "/configuration/d" ${HADOOP_HOME}/etc/hadoop/core-site.xml
cat << EOF >> ${HADOOP_HOME}/etc/hadoop/core-site.xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
EOF

sed -i "s/# export HDFS_NAMENODE_USER=hdfs/export HDFS_NAMENODE_USER=root\nexport HDFS_DATANODE_USER=root\nexport HDFS_SECONDARYNAMENODE_USER=root\nexport YARN_NODEMANAGER_USER=root\nexport YARN_RESOURCEMANAGER_USER=root\n/g" ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh
sed -i "s?# export JAVA_HOME=?export JAVA_HOME=/root/software/jdk1.8.0_371?g" ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh
# export HDFS_NAMENODE_USER=hdfs

hdfs namenode -format
start-dfs.sh
start-yarn.sh
```


