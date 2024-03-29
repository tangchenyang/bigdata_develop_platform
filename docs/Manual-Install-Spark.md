# 创建容器
## 拉取ubuntu镜像，启动容器
```shell
docker pull ubuntu:latest
```

## 启动容器
```shell
docker run -itd --privileged -p 9090:9090 --name prom ubuntu:latest
```

## 进入容器
```shell
docker exec -it prom bash
```

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

## 安装 Scala
### 下载安装包
```shell
wget  https://downloads.lightbend.com/scala/2.12.8/scala-2.12.8.tgz -P /root/install_packages/
```

### 解压
```shell
tar -zxvf /root/install_packages/scala-*.tgz -C /root/software/
```

### 配置环境变量
```shell
echo "" >> /etc/profile
echo "# scala" >> /etc/profile
echo "export SCALA_HOME=/root/software/scala-2.12.8/" >> /etc/profile
echo "export PATH=\$PATH:\$SCALA_HOME/bin" >> /etc/profile
```
### 加载环境变量
```shell
source /etc/profile
```


## 安装 Spark
### 下载安装包
```shell
wget https://archive.apache.org/dist/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz -P /root/install_packages/
wget https://mirrors.tuna.tsinghua.edu.cn/apache/spark/spark-3.3.3/spark-3.3.3-bin-hadoop3.tgz -P /root/install_packages/
```

### 解压
```shell
tar -zxvf /root/install_packages/spark-*.tgz -C /root/software/
```

### 配置环境变量
```shell
echo "" >> /etc/profile
echo "# spark" >> /etc/profile
echo "export SPARK_HOME=/root/software/spark-3.3.3-bin-hadoop3/" >> /etc/profile
echo "export PATH=\$PATH:\$SPARK_HOME/bin" >> /etc/profile
```
### 加载环境变量
```shell
source /etc/profile
```
