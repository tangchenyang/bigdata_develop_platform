#!/bin/bash
current_dir=$(cd `dirname $0` && pwd)
echo $current_dir

. $current_dir/../conf/env.sh
. $ADMINISTRATOR_HOME/conf/version.properties
if [ ! -n $COMPONENTS_HOME ]; then
  echo "COMPONENTS_HOME not found."
  exit
fi

tmp_dir=$COMPONENTS_HOME/tmp_install_package

wget -P $tmp_dir $HADOOP_DOWNLOAD_URL
tar -zxf $tmp_dir/hadoop-${HADOOP_VERSION}.tar.gz -C $COMPONENTS_HOME
rm -rf $tmp_dir

echo "# hadoop" >> ~/.bash_profile
echo "export HADOOP_HOME=$COMPONENTS_HOME/hadoop-${HADOOP_VERSION}" >> ~/.bash_profile
echo "export PATH=\$PATH:\$HADOOP_HOME/bin:\$HADOOP_HOME/sbin" >> ~/.bash_profile
. ~/.bash_profile

HADOOP_HOME=${HADOOP_HOME}
HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
HOSTNAME="hadoop"

### hadoop-env.sh
echo "<<<<<<<<<<<<<<<<< modify hadoop-env.sh ... >>>>>>>>>>>>>>>>>>>"
sed -i "s#export JAVA_HOME=\${JAVA_HOME}#export JAVA_HOME=${JAVA_HOME}#g" ${HADOOP_CONF_DIR}/hadoop-env.sh

### core-site.xml
echo "<<<<<<<<<<<<<<<<< modify core-site.xml ... >>>>>>>>>>>>>>>>>>>"
sed -i "/configuration/d" ${HADOOP_CONF_DIR}/core-site.xml
cat << EOF >> ${HADOOP_CONF_DIR}/core-site.xml
<configuration>
        <property>
                <name>fs.defaultFS</name>
                <value>hdfs://${HOSTNAME}:9000</value>
        </property>
        <property>
                <name>hadoop.tmp.dir</name>
                <value>${HADOOP_HOME}/tmp</value>
        </property>
</configuration>
EOF

### hdfs-site.xml
echo "<<<<<<<<<<<<<<<<< modify hdfs-site.xml ... >>>>>>>>>>>>>>>>>>>"
sed -i "/configuration/d" ${HADOOP_CONF_DIR}/hdfs-site.xml
cat << EOF >> ${HADOOP_CONF_DIR}/hdfs-site.xml
<configuration>
   <property>
            <name>dfs.replication</name>
            <value>2</value>
   </property>
    <property>
            <name>dfs.namenode.secondary.http-address</name>
            <value>${HOSTNAME}:9001</value>
    </property>
    <property>
            <name>dfs.namenode.name.dir</name>
            <value>file:${HADOOP_HOME}/dfs/name</value>
    </property>
    <property>
            <name>dfs.datanode.data.dir</name>
            <value>file:${HADOOP_HOME}/dfs/data</value>
    </property>
    <property>
            <name>dfs.webhdfs.enabled</name>
            <value>true</value>
    </property>
</configuration>
EOF
mkdir -p ${HADOOP_HOME}/dfs/name
mkdir -p ${HADOOP_HOME}/dfs/data

### slaves
echo "<<<<<<<<<<<<<<<<< modify slaves ... >>>>>>>>>>>>>>>>>>>"
echo -n '' > ${HADOOP_CONF_DIR}/slaves
echo "${HOSTNAME}" >> ${HADOOP_CONF_DIR}/slaves

### mapred-site.xml
echo "<<<<<<<<<<<<<<<<< modify mapred-site.xml ... >>>>>>>>>>>>>>>>>>>"
cp ${HADOOP_CONF_DIR}/mapred-site.xml.template ${HADOOP_CONF_DIR}/mapred-site.xml
sed -i "/configuration/d" ${HADOOP_CONF_DIR}/mapred-site.xml
cat << EOF >> ${HADOOP_CONF_DIR}/mapred-site.xml
<configuration>
        <property>
                <name>mapreduce.framework.name</name>
                <value>yarn</value>
        </property>
        <property>
                <name>mapreduce.jobhistory.address</name>
                <value>${HOSTNAME}:10020</value>
        </property>
        <property>
                <name>mapreduce.jobhistory.webapp.address</name>
                <value>${HOSTNAME}:19888</value>
        </property>
        <property>
                <name>mapred.job.tracker</name>
                <value>${HOSTNAME}:9001</value>
        </property>
</configuration>
EOF

### yarn-env.sh
echo "<<<<<<<<<<<<<<<<< modify yarn-env.sh ... >>>>>>>>>>>>>>>>>>>"
sed -i "s#export JAVA_HOME=#export JAVA_HOME=${JAVA_HOME}#g" ${HADOOP_CONF_DIR}/yarn-env.sh

### yarn-site.xml
echo "<<<<<<<<<<<<<<<<< modify yarn-site.xml ... >>>>>>>>>>>>>>>>>>>"
sed -i "/configuration/d" ${HADOOP_CONF_DIR}/yarn-site.xml
cat << EOF >> ${HADOOP_CONF_DIR}/yarn-site.xml
<configuration>
        <property>
                <name>yarn.nodemanager.vmem-check-enabled</name>
                <value>false</value>
        </property>
        <property>
                <name>yarn.nodemanager.aux-services</name>
                <value>mapreduce_shuffle</value>
        </property>
        <property>
                <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
                <value>org.apache.hadoop.mapred.ShuffleHandler</value>
        </property>
        <!--
        <property>
                <name>yarn.resourcemanager.address</name>
                <value>${HOSTNAME}:8032</value>
        </property>
        <property>
                <name>yarn.resourcemanager.scheduler.address</name>
                <value>${HOSTNAME}:8030</value>
        </property>
        <property>
                <name>yarn.resourcemanager.resource-tracker.address</name>
                <value>${HOSTNAME}:8031</value>
        </property>
        <property>
                <name>yarn.resourcemanager.admin.address</name>
                <value>${HOSTNAME}:8033</value>
        </property>
        <property>
                <name>yarn.resourcemanager.webapp.address</name>
                <value>${HOSTNAME}:8088</value>
        </property>
        -->
</configuration>
EOF

### format hdfs
echo "<<<<<<<<<<<<<<<<< hdfs formath ... >>>>>>>>>>>>>>>>>>>"
. ~/.bash_profile
hdfs namenode -format

### start-all
start-all.sh