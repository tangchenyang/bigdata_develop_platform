FROM ubuntu:22.04

USER root
# ssh login without password
RUN sed -i "s@ports.ubuntu.com@mirrors.aliyun.com@g" /etc/apt/sources.list && \
    apt clean && apt update
RUN apt install -y --fix-missing openssh-server vim tree net-tools
RUN /etc/init.d/ssh start &
RUN ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa -q && \
    cat ~/.ssh/*.pub > ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys && \
    sed -i "s/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/g" /etc/ssh/ssh_config

# setup Java
RUN apt install -y openjdk-8-jdk
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-arm64/
ENV PATH $PATH:$JAVA_HOME/bin

# setup Hadoop
## install Hadoop
RUN mkdir -p /root/software /root/install_packages && \
    wget https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.3.5/hadoop-3.3.5.tar.gz -P /root/install_packages/ && \
    tar -zxvf /root/install_packages/hadoop-3.3.5.tar.gz -C /root/software/ && \
    rm -f /root/install_packages/hadoop-3.3.5.tar.gz
## set env
ENV HADOOP_HOME /root/software/hadoop-3.3.5
ENV PATH $PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
## configure Hadoop
RUN mkdir -p ${HADOOP_HOME}/dfs/name ${HADOOP_HOME}/dfs/data
ADD hadoop-config/core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
ADD hadoop-config/hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
ADD hadoop-config/yarn-site.xml $HADOOP_HOME/etc/hadoop/yarn-site.xml
ADD hadoop-config/mapred-site.xml $HADOOP_HOME/etc/hadoop/mapred-site.xml
ADD hadoop-config/hadoop-env.sh $HADOOP_HOME/etc/hadoop/hadoop-env.sh
## format HDFS
RUN hdfs namenode -format
## expose YARN port
EXPOSE 8088
EXPOSE 8042
## expose HDFS port
EXPOSE 9870

# setup Hive
## install MySQL
RUN apt install -y mysql-server
ADD hive-config/mysql-change-password.sh /root/software/
RUN bash /root/software/mysql-change-password.sh
## install Hive
RUN wget https://mirrors.tuna.tsinghua.edu.cn/apache/hive/hive-4.0.1/apache-hive-4.0.1-bin.tar.gz -P /root/install_packages/ && \
    tar -zxvf /root/install_packages/apache-hive-4.0.1-bin.tar.gz -C /root/software/ && \
    rm -f /root/install_packages/apache-hive-4.0.1-bin.tar.gz
## set env
ENV HIVE_HOME /root/software/apache-hive-4.0.1-bin
ENV PATH $PATH:$HIVE_HOME/bin
## configure Hive
ADD hive-config/hive-site.xml $HIVE_HOME/conf/hive-site.xml
RUN wget -P ${HIVE_HOME}/lib https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.28/mysql-connector-java-8.0.28.jar
## expose Hive Server2 port
EXPOSE 10000

# setup Spark
## install Scala
RUN wget https://downloads.lightbend.com/scala/2.12.19/scala-2.12.19.tgz -P /root/install_packages/ && \
    tar -zxvf /root/install_packages/scala-2.12.19.tgz -C /root/software/ && \
    rm -f /root/install_packages/scala-2.12.19.tgz
## install Spark
RUN wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.5.5/spark-3.5.5-bin-hadoop3.tgz -P /root/install_packages/ && \
    tar -zxvf /root/install_packages/spark-3.5.5-bin-hadoop3.tgz -C /root/software/ && \
    rm -f /root/install_packages/spark-3.5.5-bin-hadoop3.tgz
## set env
ENV SCALA_HOME /root/software/scala-2.12.19
ENV SPARK_HOME /root/software/spark-3.5.5-bin-hadoop3
ENV PATH $PATH:$SCALA_HOME/bin:$SPARK_HOME/bin:$SPARK_HOME/sbin
## configure Spark
ADD spark-config/spark-env.sh $SPARK_HOME/conf/spark-env.sh
ADD spark-config/hive-site.xml $SPARK_HOME/conf/hive-site.xml
## expose Spark port
EXPOSE 4040
EXPOSE 15002

ADD bootstrap.sh /root/software/

# bootstrap
CMD ["bash","/root/software/bootstrap.sh", "-d"]
