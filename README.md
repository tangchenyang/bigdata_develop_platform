# 安装伪分布式Hadoop集群
## 手动安装
参考 [docker/hadoop/Hadoop-Manual-Install.md](https://github.com/tangchenyang/bigdata_develop_platform/blob/master/docker/hadoop/Hadoop-Manual-Install.md)
## DockerFile 安装
### build image
```shell
cd docker/hadoop
docker build . -t hdp:v0.1
```
### run container
```shell
docker run -itd --name hadoop -p 9870:9870 -p 8088:8088 hdp:v0.1
```
### HDFS WEB UI
[http://localhost:9870](http://localhost:9870/)

## YARN WEB UI
[http://localhost:8088](http://localhost:8088/)


--- 
# ！！！以下将废弃！！！

---


# 准备条件
- 请确保您的Linux系统能够连接互联网
- 建议 Linux 版本为 Centos 7.8 Mini 版本
- 请确保您的机器安装了git
```
yum install git -y
```

# 在任意目录（如/root/）clone 本项目
```
git clone https://github.com/tangchenyang/bigdata_develop_platform.git
``` 

# 一键安装大数据组件 
```
cd bigdata_develop_platform
bash administrator/installer/init.sh
bash administrator/installer/install.sh
```

# 运行example
```
source ~/.bash_profile
source administrator/conf/env.sh
cd applications/bin/example/moutai/
bash run_moutai.sh
```
