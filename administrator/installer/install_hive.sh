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

wget -P $tmp_dir $HIVE_DOWNLOAD_URL
mkdir $COMPONENTS_HOME/hive-${HIVE_VERSION} 
tar -zxf $tmp_dir/*hive*.tar.gz -C $COMPONENTS_HOME/hive-${HIVE_VERSION} --strip-components 1
rm -rf $tmp_dir

### env path
HIVE_HOME=$(cd $COMPONENTS_HOME/hive-${HIVE_VERSION} && pwd)
echo "# hive" >> ~/.bash_profile
echo "export HIVE_HOME=${HIVE_HOME}" >> ~/.bash_profile
echo "export PATH=\$PATH:\$HIVE_HOME/bin" >> ~/.bash_profile
. ~/.bash_profile
HIVE_CONF_DIR=${HIVE_HOME}/conf

### hive-site.xml
cp ${HIVE_CONF_DIR}/hive-default.xml.template ${HIVE_CONF_DIR}/hive-site.xml
jdbc_url=jdbc:mysql://localhost:3306/hive?createDatabaseIfNotExist=true
jdbc_driver=com.mysql.jdbc.Driver
jdbc_username=root
jdbc_password=123456
sed -i "s#jdbc:derby:;databaseName=metastore_db;create=true#${jdbc_url}#g" ${HIVE_CONF_DIR}/hive-site.xml
sed -i "s/org.apache.derby.jdbc.EmbeddedDriver/${jdbc_driver}/g" ${HIVE_CONF_DIR}/hive-site.xml
sed -i "s/APP/${jdbc_username}/g" ${HIVE_CONF_DIR}/hive-site.xml
sed -i "s#<value>mine</value>#<value>${jdbc_password}</value>#g" ${HIVE_CONF_DIR}/hive-site.xml

sed -i "s#\${system:java.io.tmpdir}#${HIVE_HOME}/temp#g" ${HIVE_CONF_DIR}/hive-site.xml
sed -i "s#\${system:user.name}#\${user.name}#g" ${HIVE_CONF_DIR}/hive-site.xml

### add driver
wget -P ${HIVE_HOME}/lib https://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.30/mysql-connector-java-5.1.30.jar

### init.sh hdfs path
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -mkdir -p /user/hive/tmp
hdfs dfs -mkdir -p /user/hive/log
hdfs dfs -chmod -R 777 /user/hive/warehouse
hdfs dfs -chmod -R 777 /user/hive/tmp
hdfs dfs -chmod -R 777 /user/hive/log

schematool -initSchema -dbType mysql

hive --service metastore &
