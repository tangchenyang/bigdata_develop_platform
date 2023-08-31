# 安装Hive
## 创建和启动 Hadoop
参考 [Manual-Install-Hadoop.md](Manual-Install-Hadoop.md)

启动后进入容器, 之后的操作均在容器内进行
```shell
docker exec -it hadoop-manual bash
```

## 安装 MySQL
### apt install
```shell
apt install -y mysql-server
```
### 启动 MySQL 服务
```shell
service mysql start
```
### 修改密码和配置
```shell
mysql -uroot << EOF
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';
EOF
```

## 安装 Hive
### 下载安装包
```shell
wget https://mirrors.tuna.tsinghua.edu.cn/apache/hive/hive-3.1.3/apache-hive-3.1.3-bin.tar.gz -P /root/install_packages/
```
### 解压
```shell
tar -zxvf /root/install_packages/apache-hive-3.1.3-bin.tar.gz -C /root/software/
```
### 配置环境变量 
```shell
echo "" >> /etc/profile
echo "# hive" >> /etc/profile
echo "export HIVE_HOME=/root/software/apache-hive-3.1.3-bin" >> /etc/profile
echo "export PATH=\$PATH:\$HIVE_HOME/bin" >> /etc/profile
```
### 加载环境变量
```shell
source /etc/profile
```

## 配置 Hive
### 拷贝配置文件
```shell
HIVE_CONF_DIR=${HIVE_HOME}/conf
cp ${HIVE_CONF_DIR}/hive-default.xml.template ${HIVE_CONF_DIR}/hive-site.xml
```
### 配置 JDBC 信息
```shell
sed -i "s#jdbc:derby:;databaseName=metastore_db;create=true#jdbc:mysql://localhost:3306/hive?createDatabaseIfNotExist=true#g" ${HIVE_CONF_DIR}/hive-site.xml
sed -i "s/org.apache.derby.jdbc.EmbeddedDriver/com.mysql.jdbc.Driver/g" ${HIVE_CONF_DIR}/hive-site.xml
sed -i "s/APP/root/g" ${HIVE_CONF_DIR}/hive-site.xml
sed -i "s#<value>mine</value>#<value>123456</value>#g" ${HIVE_CONF_DIR}/hive-site.xml
```
### 修改其他配置
```shell
# 替换异常字符
sed -i "s/\&\#8\;/ /g" ${HIVE_CONF_DIR}/hive-site.xml
# 替换系统文件路径
sed -i "s#\${system:java.io.tmpdir}#${HIVE_HOME}/temp#g" ${HIVE_CONF_DIR}/hive-site.xml
sed -i "s#\${system:user.name}#\${user.name}#g" ${HIVE_CONF_DIR}/hive-site.xml
# 关闭 doAs
sed -i '4821s/true/false/' ${HIVE_CONF_DIR}/hive-site.xml

```
### 添加 JDBC驱动
```shell
wget -P ${HIVE_HOME}/lib https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.28/mysql-connector-java-8.0.28.jar
```
### 创建 hdfs 目录
```shell
hdfs dfs -mkdir -p /user/hive/warehouse
hdfs dfs -mkdir -p /user/hive/tmp
hdfs dfs -mkdir -p /user/hive/log
hdfs dfs -chmod -R 777 /user/hive/warehouse
hdfs dfs -chmod -R 777 /user/hive/tmp
hdfs dfs -chmod -R 777 /user/hive/log
```
### 初始化元数据
```shell
schematool -initSchema -dbType mysql
```

## 启动 Hive
### Embedded CLI
```shell
hive
```
### Hive Server 2
```shell
hive --service metastore &
hiveserver2 & 
```

### Beeline
```shell
beeline -u jdbc:hive2://localhost:10000
```

