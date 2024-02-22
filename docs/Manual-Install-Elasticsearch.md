# 创建容器
## 拉取ubuntu镜像
```shell
docker pull ubuntu:latest
```

## 启动容器
```shell
docker run -itd --privileged -p 9200:9200 --name elasticsearch ubuntu:latest
```

## 进入容器
```shell
docker exec -it elasticsearch bash
```
以下操作均在容器内部

## apt install
```shell
# 国内网络切换 阿里云镜像
# sed -i "s@ports.ubuntu.com@mirrors.aliyun.com@g" /etc/apt/sources.list
apt clean && apt update
apt install -y vim wget sudo
```

# 安装 Elasticsearch 
## 下载安装包 
```shell
if [ $(uname -m ) == "aarch64"]; then
 wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.11.1-linux-aarch64.tar.gz -P /root/install_packages/
else then
 wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.11.1-linux-x86_64.tar.gz -P /root/install_packages/
fi 
```
## 解压
```shell
tar -zxvf /root/install_packages/elasticsearch-*.tar.gz -C /opt/
```

## 配置环境变量
```shell
echo "" >> /etc/profile
echo "# elasticsearch" >> /etc/profile
echo "export ELASTICSEARCH_HOME=/opt/elasticsearch-8.11.1" >> /etc/profile
echo "export PATH=\$PATH:\$ELASTICSEARCH_HOME/bin" >> /etc/profile
```
## 加载环境变量
```shell
source /etc/profile
```
## 创建 logs 和 data 目录
```shell
mkdir -p $ELASTICSEARCH_HOME/logs
mkdir -p $ELASTICSEARCH_HOME/data
```
## 创建 用户
```shell
useradd -s /bin/bash -m elasticsearch
echo "elasticsearch:123456" | sudo chpasswd
```

## 修改权限
```shell
chown -R elasticsearch:elasticsearch $ELASTICSEARCH_HOME
chmod -R 777 $ELASTICSEARCH_HOME
```


## 修改配置
```shell
# 禁用安全认证
sed -i "s/xpack.security.enabled: true/xpack.security.enabled: false/g"  $ELASTICSEARCH_HOME/config/elasticsearch.yml
```
## 启动 ES
su - elasticsearch << EOF
elasticsearch -d
EOF


## 测试 ES
```shell
curl localhost:9200
```

### 安装 head 插件
通过 Google Chrome 插件商城安装即可
