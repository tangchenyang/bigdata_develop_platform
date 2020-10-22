#!/bin/bash

wget http://dev.mysql.com/get/mysql57-community-release-el7-8.noarch.rpm

yum install mysql57-community-release-el7-8.noarch.rpm -y

yum install mysql-community-server -y

systemctl start mysqld

rm -rf mysql57-community-release-el7-8.noarch.rpm

password=$(grep 'temporary password' /var/log/mysqld.log | awk -F 'root@localhost: ' '{print $2}')

mysql -uroot -p"${password}" << EOF
set global validate_password_policy=0;
set global validate_password_length=6;
set password for 'root'@'localhost'=password('123456');
EOF
