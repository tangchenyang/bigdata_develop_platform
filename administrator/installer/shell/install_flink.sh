#!/bin/bash

FLINK_VERSION=1.11.1
### download
wget -P ~/install_pkg https://mirrors.bfsu.edu.cn/apache/flink/flink-1.11.1/flink-1.11.1-bin-scala_2.11.tgz
tar -zxf ~/install_pkg/*flink* -C ~/software

mv ~/software/*flink* ~/software/flink-${FLINK_VERSION}

### env path
FLINK_HOME=$(cd ~/software/flink-${FLINK_VERSION} && pwd)
echo "# flink" >> ~/.bash_profile
echo "export FLINK_HOME=${FLINK_HOME}" >> ~/.bash_profile
echo "export PATH=\$PATH:\$FLINK_HOME/bin" >> ~/.bash_profile
. ~/.bash_profile
FLINK_CONF_DIR=$FLINK_HOME/conf


###
