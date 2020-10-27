#!/bin/bash
installer_dir=$(cd `dirname $0`/.. && pwd)
echo $installer_dir

# install wget
yum install wget -y

# install vim
yum install vim -y

# ssh
rm -rf ~/.ssh
ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa -q
cat ~/.ssh/*.pub > ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
sed -i "s/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/g" /etc/ssh/ssh_config

# fireware
systemctl stop firewalld.service
systemctl disable firewalld.service
sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config

# hostname
echo 'hadoop' > /etc/hostname
hostname hadoop
