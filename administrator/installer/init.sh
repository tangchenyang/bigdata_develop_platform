#!/bin/bash
# init folder
mkdir -p ~/install_pkg
mkdir -p ~/software

# install wget
yum install wget -y

# install vim
yum install vim -y

# ssh
rm -rf ~/.ssh
ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa -q
cat ~/.ssh/*.pub > ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys

# fireware
systemctl stop firewalld.service
systemctl disable firewalld.service
sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config

# hostname
echo 'localhost' > /etc/hostname
hostname localhost