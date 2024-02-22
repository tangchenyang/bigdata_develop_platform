# 创建容器
## 拉取ubuntu镜像
```shell
docker pull ubuntu:latest
```

## 启动容器
```shell
docker run -itd --privileged -p 5601:5601 --name logstash ubuntu:latest
```

## 进入容器
```shell
docker exec -it logstash bash
```
以下操作均在容器内部

## apt install
```shell
# 国内网络切换 阿里云镜像
# sed -i "s@ports.ubuntu.com@mirrors.aliyun.com@g" /etc/apt/sources.list
apt clean && apt update
apt install -y vim wget 
```

# 安装 Logstash
## 创建用于存放安装包和软件的目录
```shell
mkdir -p /root/software
mkdir -p /root/install_packages
```

## 下载安装包
```shell
if [ $(uname -m ) == "aarch64"]; then
 wget https://artifacts.elastic.co/downloads/logstash/logstash-8.11.1-linux-aarch64.tar.gz -P /root/install_packages/
else then
 wget https://artifacts.elastic.co/downloads/logstash/logstash-8.11.1-linux-x86_64.tar.gz -P /root/install_packages/
fi 
```

## 解压
```shell
tar -zxvf /root/install_packages/logstash-*.tar.gz -C /root/software/
```

## 配置环境变量
```shell
echo "" >> /etc/profile
echo "# logstash" >> /etc/profile
echo "export LOGSTASH_HOME=/root/software/logstash-8.11.1" >> /etc/profile
echo "export PATH=\$PATH:\$LOGSTASH_HOME/bin" >> /etc/profile
```
## 加载环境变量
```shell
source /etc/profile
```

## 测试Logstash
#### 通过命令行运行
```shell
logstash -e 'input { stdin { } } output { stdout {} }'
```

