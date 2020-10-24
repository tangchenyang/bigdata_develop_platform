#!/bin/bash
SCALA_VERSION=2.11.12

wget -P ~/install_pkg https://downloads.lightbend.com/scala/${SCALA_VERSION}/scala-${SCALA_VERSION}.tgz
tar -zxf ~/install_pkg/*scala* -C ~/software

### env path
SCALA_HOME=$(cd ~/software/scala-${SCALA_VERSION} && pwd)
echo "# scala" >> ~/.bash_profile
echo "export SCALA_HOME=${SCALA_HOME}" >> ~/.bash_profile
echo "export PATH=\$PATH:\$SCALA_HOME/bin" >> ~/.bash_profile