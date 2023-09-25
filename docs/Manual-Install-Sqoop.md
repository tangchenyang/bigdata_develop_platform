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
hive -e "CREATE TABLE IF NOT EXISTS test_1(tid STRING);CREATE TABLE IF NOT EXISTS test_2(tid STRING);"

## import from mysql 
hdfs dfs -rm -r /user/hive/warehouse/HIVE_TBLS
hive -e "drop table hive_tbls"
sqoop import \
  --connect jdbc:mysql://localhost/hive \
  --username root \
  --password 123456 \
  --table TBLS \
  -m 1 \
  --hive-import \
  --hive-overwrite \
  --create-hive-table \
  --hive-table hive_tbls \
  --target-dir /user/hive/warehouse/HIVE_TBLS \
  -m 1 
  
## Mock ETL
hive -e "DROP TABLE hive_tbls_export; CREATE TABLE hive_tbls_export AS SELECT tbl_name, tbl_type from hive_tbls;"

## export to mysql
mysql -uroot -p123456 << EOF
create database report;
create table report.hive_tbls_export(tbl_name varchar(255), tbl_type varchar(255));
EOF

sqoop export \
--connect jdbc:mysql://localhost/report \
--driver com.mysql.jdbc.Driver \
--username root \
--password 123456 \
--table hive_tbls_export \
--hcatalog-table hive_tbls_export \
--input-fields-terminated-by ',' \
--num-mappers 1
```
