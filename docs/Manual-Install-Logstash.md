# 创建容器
## 拉取ubuntu镜像，启动容器
```shell
docker pull ubuntu:latest
```

## 启动容器
```shell
docker run -itd --privileged -p 9200:9200 -p 5044:5044 -p 5601:5601 --name elk ubuntu:latest
```

## 进入容器
```shell
docker exec -it elk bash
```
以下操作均在容器内部

# 配置 SSH 免密
## 安装SSH服务
```shell
# 国内网络切换 阿里云镜像
# sed -i "s@ports.ubuntu.com@mirrors.aliyun.com@g" /etc/apt/sources.list
apt clean && apt update
apt install -y vim openssh-server 
/etc/init.d/ssh start
```

## ssh 免密 
```shell
ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa -q
cat ~/.ssh/*.pub > ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys
sed -i "s/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/g" /etc/ssh/ssh_config  
```

# 安装软件
## 创建用于存放安装包和软件的目录
```shell
mkdir -p /root/software
mkdir -p /root/install_packages
```

## 安装 JDK 
### apt 安装 jdk8
```shell
apt install -y openjdk-8-jdk
```

### 配置 JAVA_HOME 
```shell
echo "" >> /etc/profile
echo "# java" >> /etc/profile
echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64/" >> /etc/profile
echo "export PATH=\$PATH:\$JAVA_HOME/bin" >> /etc/profile
```

## 安装 Logstash
### 下载安装包
```shell
if [ $(uname -m ) == "aarch64"]; then
 wget https://artifacts.elastic.co/downloads/logstash/logstash-8.11.1-linux-aarch64.tar.gz -P /root/install_packages/
else then
 wget https://artifacts.elastic.co/downloads/logstash/logstash-8.10.4-linux-x86_64.tar.gz -P /root/install_packages/
fi 
```

### 解压
```shell
tar -zxvf /root/install_packages/logstash-*.tar.gz -C /root/software/
```

### 配置环境变量
```shell
echo "" >> /etc/profile
echo "# logstash" >> /etc/profile
echo "export LOGSTASH_HOME=/root/software/logstash-8.11.1" >> /etc/profile
echo "export PATH=\$PATH:\$LOGSTASH_HOME/bin" >> /etc/profile
```
### 加载环境变量
```shell
source /etc/profile
```

### 测试Logstash
#### 通过命令行运行
```shell
logstash -e 'input { stdin { } } output { stdout {} }'
```

#### 通过配置文件运行
创建 pipeline config 
```shell

```
指定 config 运行
```shell

```

## 安装 Elasticsearch 
### 下载安装包 
```shell
if [ $(uname -m ) == "aarch64"]; then
 wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.11.1-linux-aarch64.tar.gz -P /root/install_packages/
else then
 wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.11.1-linux-x86_64.tar.gz -P /root/install_packages/
fi 
```
### 解压
```shell
tar -zxvf /root/install_packages/elasticsearch-*.tar.gz -C /root/software/
```

### 配置环境变量
```shell
echo "" >> /etc/profile
echo "# elasticsearch" >> /etc/profile
echo "export ELASTICSEARCH_HOME=/root/software/elasticsearch-8.11.1" >> /etc/profile
echo "export PATH=\$PATH:\$ELASTICSEARCH_HOME/bin" >> /etc/profile
```
### 加载环境变量
```shell
source /etc/profile
```
### 创建 logs 和 data 目录
```shell
mkdir -p $ELASTICSEARCH_HOME/logs
mkdir -p $ELASTICSEARCH_HOME/data
```
### 创建 用户
```shell
useradd elasticsearch
echo 'elasticsearch' | passwd --stdin elasticsearch
echo "elasticsearch:123456" | sudo chpasswd
```

### 修改权限
```shell
chown -R elasticsearch:elasticsearch $ELASTICSEARCH_HOME
chmod -R 777 $ELASTICSEARCH_HOME
```
### 测试 ES

### 安装 head 插件

