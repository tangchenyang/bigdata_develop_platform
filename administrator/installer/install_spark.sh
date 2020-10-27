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

wget -P $tmp_dir $SPARK_DOWNLOAD_URL
mkdir $COMPONENTS_HOME/spark-${SPARK_VERSION}
tar -zxf $tmp_dir/*spark* -C $COMPONENTS_HOME/spark-${SPARK_VERSION} --strip-components 1
rm -rf $tmp_dir

### env path
SPARK_HOME=$(cd $COMPONENTS_HOME/spark-${SPARK_VERSION} && pwd)
echo "# spark" >> ~/.bash_profile
echo "export SPARK_HOME=${SPARK_HOME}" >> ~/.bash_profile
echo "export PATH=\$PATH:\$SPARK_HOME/bin" >> ~/.bash_profile

. ~/.bash_profile

SPARK_CONF_DIR=${SPARK_HOME}/conf
### spark-env.sh

cp ${SPARK_CONF_DIR}/spark-env.sh.template ${SPARK_CONF_DIR}/spark-env.sh
echo "export JAVA_HOME=${JAVA_HOME}" >> ${SPARK_CONF_DIR}/spark-env.sh
echo "export SCALA_HOME=${SCALA_HOME}" >> ${SPARK_CONF_DIR}/spark-env.sh
echo "export HADOOP_HOME=${HADOOP_HOME}" >> ${SPARK_CONF_DIR}/spark-env.sh
echo "export HADOOP_CONF_DIR=${HADOOP_HOME}/etc/hadoop" >> ${SPARK_CONF_DIR}/spark-env.sh
echo "export SPARK_HOME=${SPARK_HOME}" >> ${SPARK_CONF_DIR}/spark-env.sh

### hive-site.xml
echo "<<<<<<<<<<<<<<<<< add hive-site.xml ... >>>>>>>>>>>>>>>>>>>"
cat << EOF >> ${SPARK_CONF_DIR}/hive-site.xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
  <property>
    <name>hive.metastore.uris</name>
    <value>thrift://hadoop:9083</value>
    <description>Thrift URI for the remote metastore. Used by metastore client to connect to remote metastore.</description>
  </property>
</configuration>
EOF
