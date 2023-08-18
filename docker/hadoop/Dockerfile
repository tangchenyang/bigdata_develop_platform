FROM ubuntu:latest

USER root
# ssh login without password
RUN apt update && apt install -y openssh-server vim
RUN /etc/init.d/ssh start &
RUN ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa -q && \
    cat ~/.ssh/*.pub > ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && \
    sed -i "s/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/g" /etc/ssh/ssh_config

# install jdk
RUN apt install -y openjdk-8-jdk
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-arm64/
ENV PATH $PATH:$JAVA_HOME/bin

# install hadoop
RUN mkdir -p /root/software /root/install_packages
RUN wget https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.3.5/hadoop-3.3.5.tar.gz -P /root/install_packages/
RUN tar -zxvf /root/install_packages/hadoop-3.3.5.tar.gz -C /root/software/
ENV HADOOP_HOME /root/software/hadoop-3.3.5
ENV PATH $PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# configure hadoop
RUN mkdir -p ${HADOOP_HOME}/dfs/name ${HADOOP_HOME}/dfs/data
ADD core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
ADD hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
ADD yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml
ADD mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml
RUN sed -i "s/# export HDFS_NAMENODE_USER=hdfs/export HDFS_NAMENODE_USER=root\nexport HDFS_DATANODE_USER=root\nexport HDFS_SECONDARYNAMENODE_USER=root\nexport YARN_NODEMANAGER_USER=root\nexport YARN_RESOURCEMANAGER_USER=root\n/g" ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh && \
    sed -i "s?# export JAVA_HOME=?export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64?g" ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

# format hdfs
RUN hdfs namenode -format

# YARN port
EXPOSE 8088
# HDFS port
EXPOSE 9870

ADD bootstrap.sh /root/software/

# start hadoop
CMD ["bash","/root/software/bootstrap.sh", "-d"]
