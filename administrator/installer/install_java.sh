#!/bin/bash
yum install java-1.8* -y
echo "# java" >> ~/.bash_profile
echo "export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.262.b10-0.el7_8.x86_64/jre/" >>  ~/.bash_profile
echo "export PATH=\$PATH:\$JAVA_HOME/bin" >>  ~/.bash_profile
. ~/.bash_profile
java -version