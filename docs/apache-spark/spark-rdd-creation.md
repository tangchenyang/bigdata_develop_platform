# 创建 RDD
创建RDD的方式主要有两种：通过并行化现有的集合创建 RDD ；或者通过读取外部系统如 HDFS 等创建 RDD。  
本篇文章的后续实践可在 spark-shell 中完成, 其中会默认实例化一个 SparkContext 实例 `sc` 和 SparkSession 实例 `spark`。
```shell
spark-shell
```
## 并行化现有集合 
根据内存中的集合来生成RDD
```
scala> val scalaList = List("A", "B", "C", "D", "E", "F")
scalaList: List[String] = List(A, B, C, D, E, F)

scala> val sparkRDD =  sc.parallelize(scalaList, 3)
sparkRDD: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:24

scala> sparkRDD.partitions.size
res0: Int = 3
```
并行化现有集合相关其他算子  
- range
- makeRDD  
- emptyRDD: no partitions or elements.

## 读取外部系统数据   
从外部系统重读取数据来生成RDD
``` 
scala> val rddFromLocalFS = sc.textFile("file:///root/software/spark-3.5.1-bin-hadoop3/README.md")
rddFromLocalFS: org.apache.spark.rdd.RDD[String] = file:///root/software/spark-3.5.1-bin-hadoop3/README.txt MapPartitionsRDD[0] at textFile at <console>:23

scala> val rddFromHDFS = sc.textFile("hdfs:///README.txt")
rddFromHDFS: org.apache.spark.rdd.RDD[String] = hdfs:///README.txt MapPartitionsRDD[1] at textFile at <console>:23

scala> val rddFromHDFS = sc.textFile("/README.txt")
rddFromHDFS: org.apache.spark.rdd.RDD[String] = /README.txt MapPartitionsRDD[2] at textFile at <console>:23
```
读取外部系统相关其他算子
- wholeTextFiles
- binaryFiles
- hadoopRDD
- hadoopFile
- newAPIHadoopFile
- sequenceFile
- objectFile  
