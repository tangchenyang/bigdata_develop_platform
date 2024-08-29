# Spark RDD - Control 算子
## persist
将 RDD 缓存到内存或者磁盘中，通过读取缓存中的数据避免重复读取外部系统，从而提升作业性能
``` 
scala> val rddFromLocalFS = sc.textFile("file:///root/software/spark-3.5.1-bin-hadoop3/README.md")
rddFromLocalFS: org.apache.spark.rdd.RDD[String] = file:///root/software/spark-3.5.1-bin-hadoop3/README.md MapPartitionsRDD[0] at textFile at <console>:25

scala> rddFromLocalFS.persist(org.apache.spark.storage.StorageLevel.MEMORY_AND_DISK)
res0: rddFromLocalFS.type = file:///root/software/spark-3.5.1-bin-hadoop3/README.md MapPartitionsRDD[1] at textFile at <console>:25

scala> rddFromLocalFS.count
res1: Long = 125
```
## cache
等同于缓存级别为 `MEMORY_ONLY` 的 [persist](#persist)  
## unpersist
将已经缓存的 RDD 解除缓存，以释放当前作业的内存或磁盘空间  
``` 
scala> val rddFromLocalFS = sc.textFile("file:///root/software/spark-3.5.1-bin-hadoop3/README.md")
rddFromLocalFS: org.apache.spark.rdd.RDD[String] = file:///root/software/spark-3.5.1-bin-hadoop3/README.md MapPartitionsRDD[0] at textFile at <console>:25

scala> rddFromLocalFS.persist(org.apache.spark.storage.StorageLevel.MEMORY_AND_DISK)
res0: rddFromLocalFS.type = file:///root/software/spark-3.5.1-bin-hadoop3/README.md MapPartitionsRDD[1] at textFile at <console>:25

scala> rddFromLocalFS.unpersist()
```
## checkpoint
将当前 RDD 保存在设置的 checkpointDir 中，并移除对父 RDD 的血缘关系，当发生故障时，无需再从父 RDD 重新计算。 
``` 
scala> val rddFromLocalFS = sc.textFile("file:///root/software/spark-3.5.1-bin-hadoop3/README.md")
rddFromLocalFS: org.apache.spark.rdd.RDD[String] = file:///root/software/spark-3.5.1-bin-hadoop3/README.md MapPartitionsRDD[0] at textFile at <console>:25

scala> rddFromLocalFS.cache()
res0: rddFromLocalFS.type = file:///root/software/spark-3.5.1-bin-hadoop3/README.md MapPartitionsRDD[1] at textFile at <console>:25

scala> sc.setCheckpointDir("/tmp/spark/app-checkpoint/")

scala> rddFromLocalFS.checkpoint

scala> rddFromLocalFS.count
res1: Long = 125
```
