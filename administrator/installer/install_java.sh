#!/bin/bash
current_dir=$(cd `dirname $0` && pwd)
echo $current_dir

. $current_dir/../conf/env.sh
. $ADMINISTRATOR_HOME/conf/version.properties

yum install java-${JAVA_VERSION}* -y

echo "# java" >> ~/.bash_profile
echo "export JAVA_HOME=/usr/lib/jvm/$(ls /usr/lib/jvm/ | grep openjdk-${JAVA_VERSION})/jre/" >>  ~/.bash_profile
echo "export PATH=\$PATH:\$JAVA_HOME/bin" >>  ~/.bash_profile
. ~/.bash_profile
java -version