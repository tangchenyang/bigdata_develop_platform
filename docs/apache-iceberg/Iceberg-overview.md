# Iceberg 简介

## 什么是 Iceberg

Iceberg 是一种狭义上的数据湖组件，常应用于数仓和数据湖架构中，可以支持行级别的更新操作，就像他的名字一样，用户可以只对想要的那部分数据行进行操作   
![image](https://github.com/tangchenyang/picx-images-hosting/raw/master/20240902/image.1hs5m2yz2w.webp)

Iceberg 事实上是一种表格式或者说表的管理方式，其自身会管理表的元数据信息，而不强依赖于
Catalog，并且对表的数据文件进行了全新的组织  
我们来对比一下与 Hive/Athena 的目录结构

- Hive 的数据文件结构，元数据在 Catalog 中，如 Glue 或者 Hive MetaStore 等，数据保存在 HDFS/S3 等文件系统中
  - Glue Catalog: MetaData
  - S3: Data files location <tableLocation>/partition1=../partition2=../*.parquet
- Iceberg 的数据文件结构
  - Glue Catalog: simple table info, like dbName, tableName, location ..
  - S3:
    - metadata location:
      - metadata file
      - snapshot(manifest list)
      - manifest
    - data
      - partition1

在数据湖/数据仓库中的位置
todo 位置图  

- 支持与多种计算引擎集成  
  - AWS Athena  
    - 删除模式为 merge-on-read  
    - 简化操作，仅保留更少量的必要的配置项  
  - Spark  
    - 
  - Flink
  - ...

## 为什么需要 Iceberg  
我们已经有很多可以通过SQL来操作数据的组件，比如 Athena，那为什么还需要 Iceberg 呢，那我们先来分析一下传统数据仓库组件都有哪些痛点  
- 传统的痛点  
  - 操作都是基于文件级别甚至目录级别的读写，不支持常规的更新和删除语义，要实现更新、删除，需要将整个分区甚至整张表的数据重新覆写
  - 全表覆盖时，整张表将处于不可用的状态  
  - 元数据与数据分开管理，容易造成不一致的问题
  - 需要频繁与 MetaStore 交互，listPartitions 很慢
  - 对象存储的 listFiles 很耗时
这些缺点在离线计算的领域通常不致命，因为离线计算对性能的要求没有那么的高，只要在DA工作期间能看到前一天的数据即可。  
但是在实时计算的领域就非常致命，比如我们要求的延迟是小时级别的，即当前查询的时候应当能看到前一个小时的数据，而计算本身又花费了50分钟，那么 DA 能看到数据时，已经应接近两个小时的延迟了。  
并且当计算时间超过计算间隔时，任务将排队，
- Iceberg 的优缺点
  - 更新/删除数据的成本更低，延迟更低
  - 用户无需考虑表的元数据与数据间的一致性问题

## 与数据仓库组件对比

## 与其他数据湖组件对比
## Iceberg 是如何工作的

- Iceberg on Athena
- Iceberg on Spark


## Iceberg 与 Spark 集成


