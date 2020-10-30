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

wget -P $tmp_dir $SQOOP_DOWNLOAD_URL
mkdir $COMPONENTS_HOME/sqoop-${SQOOP_VERSION}
tar -zxf $tmp_dir/*sqoop* -C $COMPONENTS_HOME/sqoop-${SQOOP_VERSION} --strip-components 1
rm -rf $tmp_dir

### env path
SQOOP_HOME=$(cd $COMPONENTS_HOME/sqoop-${SQOOP_VERSION} && pwd)
echo "# sqoop" >> ~/.bash_profile
echo "export SQOOP_HOME=${SQOOP_HOME}" >> ~/.bash_profile
echo "export PATH=\$PATH:\$SQOOP_HOME/bin" >> ~/.bash_profile

. ~/.bash_profile

SQOOP_CONF_DIR=${SQOOP_HOME}/conf
### add driver
wget -P ${SQOOP_HOME}/lib https://repo1.maven.org/maven2/mysql/mysql-connector-java/5.1.30/mysql-connector-java-5.1.30.jar

### add hive-common
cp $HIVE_HOME/lib/hive-common-${HIVE_VERSION}.jar $SQOOP_HOME/lib/

### sqoop-env.sh
cp ${SQOOP_CONF_DIR}/sqoop-env-template.sh ${SQOOP_CONF_DIR}/sqoop-env.sh
echo "export HADOOP_COMMON_HOME=${HADOOP_HOME}" >> ${SQOOP_CONF_DIR}/sqoop-env.sh
echo "export HADOOP_MAPRED_HOME=${HADOOP_HOME}" >> ${SQOOP_CONF_DIR}/sqoop-env.sh
echo "export HIVE_HOME=${HIVE_HOME}" >> ${SQOOP_CONF_DIR}/sqoop-env.sh

