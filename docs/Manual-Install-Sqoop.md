# 安装 Hadoop 和 Hive
## 安装 Hadoop
参考 [Manual-Install-Hadoop.md](Manual-Install-Hadoop.md)

## 安装 Hive 
参考 [Manual-Install-Hive.md](Manual-Install-Hive.md)

# 安装 Sqoop
## 下载安装包
```shell
wget https://archive.apache.org/dist/sqoop/1.4.7/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz -P /root/install_packages/
```

## 解压
```shell
tar -zxvf /root/install_packages/sqoop-1.4.7.bin__hadoop-2.6.0.tar.gz -C /root/software/

```

## 配置环境变量 
```shell
echo "" >> /etc/profile
echo "# sqoop" >> /etc/profile
echo "export SQOOP_HOME=/root/software/sqoop-1.4.7.bin__hadoop-2.6.0" >> /etc/profile
echo "export PATH=\$PATH:\$SQOOP_HOME/bin" >> /etc/profile
```
## 加载环境变量
```shell
source /etc/profile
```


## 下载 JDBC 驱动
```shell
# MySQL
wget -P ${SQOOP_HOME}/lib https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.28/mysql-connector-java-8.0.28.jar
wget -P ${SQOOP_HOME}/lib https://jdbc.postgresql.org/download/postgresql-42.5.4.jar
```

## sqoop-env.sh
```shell
SQOOP_CONF_DIR=${SQOOP_HOME}/conf
cp ${SQOOP_CONF_DIR}/sqoop-env-template.sh ${SQOOP_CONF_DIR}/sqoop-env.sh
echo "export HADOOP_COMMON_HOME=${HADOOP_HOME}" >> ${SQOOP_CONF_DIR}/sqoop-env.sh
echo "export HADOOP_MAPRED_HOME=${HADOOP_HOME}" >> ${SQOOP_CONF_DIR}/sqoop-env.sh
echo "export HIVE_HOME=${HIVE_HOME}" >> ${SQOOP_CONF_DIR}/sqoop-env.sh
echo "export HIVE_CONF_DIR=${HIVE_HOME}/conf" >> ${SQOOP_CONF_DIR}/sqoop-env.sh
echo "export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$HIVE_HOME/lib/*" >> ${SQOOP_CONF_DIR}/sqoop-env.sh
```

## sqoop version
```shell
sqoop version
```

## Other Example cmd
### list databases
```shell
sqoop list-databases --connect jdbc:mysql://localhost:3306/hive --username root --password 123456
```

```shell
## 爬取数据
mkdir /root/workspace 

apt update && apt install -y curl 
curl -XGET 'https://so.gushiwen.cn/gushi/tangshi.aspx' > /root/workspace/tangpoems.html
cat /root/workspace/tangpoems.html | grep 'shiwenv' | awk -F '<|>' '{print $5","$7}' > /root/workspace/tangpoems.csv


## set utf-8 以避免中文乱码
cat << EOF >> /etc/mysql/my.cnf
[mysqld]
character-set-server=utf8 
local-infile 
[client]
default-character-set=utf8 
local-infile 
[mysql]
default-character-set=utf8
local-infile 
EOF
service mysql restart

## 导入 数据到MySQL
mysql -uroot -p123456 --local-infile=1 << EOF
SET GLOBAL local_infile=1;
create database if not exists data;
create table if not exists data.tang_poems_300(poem varchar(255), author varchar(255)) default charset=utf8;
LOAD DATA LOCAL INFILE '/root/workspace/tangpoems.csv' INTO TABLE data.tang_poems_300 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
EOF

## import from mysql 
hdfs dfs -rm -r /user/hive/warehouse/ODS_TANG_POEMS_300
hive -e "drop table ods_tang_poem_300"
sqoop import \
  --connect jdbc:mysql://localhost/data \
  --username root \
  --password 123456 \
  --table tang_poems_300 \
  -m 1 \
  --hive-import \
  --hive-overwrite \
  --create-hive-table \
  --hive-table ods_tang_poem_300 \
  --target-dir /user/hive/warehouse/ODS_TANG_POEMS_300 \
  -m 1 
  
## Mock ETL
## DWD
hive -e "
DROP TABLE IF EXISTS dwd_tang_poem_300; 
CREATE TABLE dwd_tang_poem_300 AS 
  SELECT poem, REGEXP_REPLACE(author,'\\\\(|\\\\)', '') AS author
    FROM ods_tang_poem_300
;
"
## DWS

hive -e "
DROP TABLE IF EXISTS dws_poem_num_by_author; 
CREATE TABLE dws_poem_num_by_author AS 
  SELECT author, count(1) AS poem_num 
    FROM dwd_tang_poem_300
GROUP BY author 
ORDER by poem_num DESC
;
"
## export to mysql
# create ads db and table
mysql -uroot -p123456 << EOF
create database ads;
create table ads.ads_poem_num_by_author(author varchar(255), poem_num int);
EOF

sqoop export \
--connect jdbc:mysql://localhost/ads \
--driver com.mysql.jdbc.Driver \
--username root \
--password 123456 \
--table ads_poem_num_by_author \
--hcatalog-table dws_poem_num_by_author \
--input-fields-terminated-by ',' \
--num-mappers 1 

## 提前在PG中创建表
create table ads_poem_num_by_author(author varchar(255), poem_num bigint);


## export to postgres
sqoop export \
--connect jdbc:postgresql://postgres:5432/postgres \
--driver org.postgresql.Driver \
--username postgres \
--password 123456 \
--table ads_poem_num_by_author \
--hcatalog-table dws_poem_num_by_author \
--input-fields-terminated-by ',' \
--num-mappers 1 
```
