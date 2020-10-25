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

wget -P $tmp_dir $FLINK_DOWNLOAD_URL
mkdir $COMPONENTS_HOME/flink-${FLINK_VERSION}
tar -zxf $tmp_dir/*flink* -C $COMPONENTS_HOME/flink-${FLINK_VERSION} --strip-components 1
rm -rf $tmp_dir

### env path
FLINK_HOME=$(cd $COMPONENTS_HOME/flink-${FLINK_VERSION} && pwd)
echo "# flink" >> ~/.bash_profile
echo "export FLINK_HOME=${FLINK_HOME}" >> ~/.bash_profile
echo "export PATH=\$PATH:\$FLINK_HOME/bin" >> ~/.bash_profile
. ~/.bash_profile
FLINK_CONF_DIR=$FLINK_HOME/conf


###
