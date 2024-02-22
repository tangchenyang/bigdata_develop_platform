# 创建容器
## 拉取ubuntu镜像
```shell
docker pull ubuntu:latest
```

## 启动容器
```shell
docker run -itd --privileged -p 5601:5601 --name kibana ubuntu:latest
```

## 进入容器
```shell
docker exec -it kibana bash
```
以下操作均在容器内部

## apt install
```shell
# 国内网络切换 阿里云镜像
# sed -i "s@ports.ubuntu.com@mirrors.aliyun.com@g" /etc/apt/sources.list
apt clean && apt update
apt install -y vim wget curl 
```

# 安装 Kibana
## 创建用于存放安装包和软件的目录
```shell
mkdir -p /root/software
mkdir -p /root/install_packages
```

## 下载安装包
```shell
if [ $(uname -m ) == "aarch64"]; then
 wget https://artifacts.elastic.co/downloads/kibana/kibana-8.11.1-linux-aarch64.tar.gz -P /root/install_packages/
else then
 wget https://artifacts.elastic.co/downloads/kibana/kibana-8.11.1-linux-x86_64.tar.gz -P /root/install_packages/
fi 
```

## 解压
```shell
tar -zxvf /root/install_packages/kibana-*.tar.gz -C /root/software/
```

## 配置环境变量
```shell
echo "" >> /etc/profile
echo "# kibana" >> /etc/profile
echo "export KIBANA_HOME=/root/software/kibana-8.11.1" >> /etc/profile
echo "export PATH=\$PATH:\$KIBANA_HOME/bin" >> /etc/profile
```

## 加载环境变量
```shell
source /etc/profile
```

## 配置 Kibana
```shell
server.host: 0.0.0.0
```
## 启动
```shell
kibana --allow-root & 
```

## 测试
```shell
curl localhost:5601
```

