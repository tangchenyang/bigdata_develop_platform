# syntax = docker/dockerfile:1.4.0

FROM hdp:v0.1

USER root

RUN apt install -y mysql-server

RUN wget https://mirrors.tuna.tsinghua.edu.cn/apache/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz -P /root/install_packages/

RUN tar -zxvf /root/install_packages/apache-hive-3.1.3-bin.tar.gz -C /root/software/
ENV HIVE_HOME /root/software/apache-hive-3.1.3-bin
ENV PATH $PATH:$HIVE_HOME/bin

ENV HIVE_CONF_DIR $HIVE_HOME/conf
RUN cp ${HIVE_CONF_DIR}/hive-default.xml.template ${HIVE_CONF_DIR}/hive-site.xml

RUN sed -i "s#jdbc:derby:;databaseName=metastore_db;create=true#jdbc:mysql://localhost:3306/hive?createDatabaseIfNotExist=true#g" ${HIVE_CONF_DIR}/hive-site.xml &&  \
    sed -i "s/org.apache.derby.jdbc.EmbeddedDriver/com.mysql.jdbc.Driver/g" ${HIVE_CONF_DIR}/hive-site.xml &&  \
    sed -i "s/APP/root/g" ${HIVE_CONF_DIR}/hive-site.xml &&  \
    sed -i "s#<value>mine</value>#<value>123456</value>#g" ${HIVE_CONF_DIR}/hive-site.xml

RUN sed -i "s/\&\#8\;/ /g" ${HIVE_CONF_DIR}/hive-site.xml &&  \
    sed -i "s#\${system:java.io.tmpdir}#${HIVE_HOME}/temp#g" ${HIVE_CONF_DIR}/hive-site.xml &&  \
    sed -i "s#\${system:user.name}#\${user.name}#g" ${HIVE_CONF_DIR}/hive-site.xml &&  \
    sed -i '4821s/true/false/' ${HIVE_CONF_DIR}/hive-site.xml

RUN wget -P ${HIVE_HOME}/lib https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.28/mysql-connector-java-8.0.28.jar


ADD mysql-change-password.sh /root/software/
RUN bash /root/software/mysql-change-password.sh

#RUN hdfs dfs -mkdir -p /user/hive/warehouse &&  \
#    hdfs dfs -mkdir -p /user/hive/tmp &&  \
#    hdfs dfs -mkdir -p /user/hive/log && \
#    hdfs dfs -chmod -R 777 /user/hive/warehouse && \
#    hdfs dfs -chmod -R 777 /user/hive/tmp &&  \
#    hdfs dfs -chmod -R 777 /user/hive/log \


EXPOSE 10000

ADD bootstrap-hive.sh /root/software/

# start hadoop
CMD ["bash", "/root/software/bootstrap-hive.sh", "-d"]


