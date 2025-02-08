#!/bin/bash
# 启动平台， 启动所有组件
# hadoop
start-all.sh

#hive
hive --service metastore &
