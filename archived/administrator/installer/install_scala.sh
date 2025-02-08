#!/bin/bash
current_dir=$(cd `dirname $0` && pwd)
. $current_dir/../conf/env.sh
. $ADMINISTRATOR_HOME/conf/version.properties
if [ ! -n $COMPONENTS_HOME ]; then
  echo "COMPONENTS_HOME not found."
  exit
fi

tmp_dir=$COMPONENTS_HOME/tmp_install_package

wget -P $tmp_dir $SCALA_DOWNLOAD_URL
mkdir $COMPONENTS_HOME/scala-${SCALA_VERSION}
tar -zxf $tmp_dir/*scala* -C $COMPONENTS_HOME
rm -rf $tmp_dir

### env path
SCALA_HOME=$(cd $COMPONENTS_HOME/scala-${SCALA_VERSION} && pwd)
echo "# scala" >> ~/.bash_profile
echo "export SCALA_HOME=${SCALA_HOME}" >> ~/.bash_profile
echo "export PATH=\$PATH:\$SCALA_HOME/bin" >> ~/.bash_profile
