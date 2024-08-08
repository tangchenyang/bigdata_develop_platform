# Spark RDD
## RDD 简介
RDD(Resilient Distributed Dataset) - 弹性分布式数据集，是 Spark 用来并行操作跨节点数据的主要抽象  
### RDD的五大特性
1. 一组分区：每个RDD拥有一组partitions, 每个partition将由一个task来处理
2. 数据血缘：每个RDD记录了其依赖关系，可向上追溯父RDD，发生错误时，可从父RDD开始重新计算
3. 转换函数：每个RDD拥有其转换函数，记录了其是怎样通过父RDD转换而来的
4. 分区器：每个RDD拥有一个Partitioner, 记录了其重新分区的规则
5. 数据本地性：移动计算优于移动数据，RDD会尽可能让计算task发生在离数据更近的地方
### Shuffle 操作
Shuffle 是 Spark 进行数据交换或者说重新分配数据的一种操作，这通常会产生跨 Executor 、跨节点，甚至跨机房、跨地区的数据拷贝，因此 Shuffle 操作的成本一来说都比较高  
只有宽依赖(Wide-Dependency)算子会产生Shuffle, 窄依赖(Narrow-Dependency)算子不会产生Shuffle    

![image](https://github.com/tangchenyang/picx-images-hosting/raw/master/20240808/image.5c0w5b3q3u.webp)   

#### 窄依赖  
父RDD的每一个分区，最多只会被子RDD的一个分区所依赖，这意味着在计算过程中，当前partition中的数据，不需要与其他partitions中的数据进行交互，即可完成计算  
因为不涉及Shuffle，这类算的的计算速度一般都很快；也以为其一对一的特点，多个相邻的窄依赖算子可以被Chain起来，放在一个Stage中，形成一个优化的流水线
常见的窄依赖算子有 map, filter, union 等
#### 宽依赖
父RDD的每一个分区，会被自RDD的多个分区所依赖, 这意味着当前partition中的数据，会按需(partitioner)被重新分配到子RDD的不同各个partition中，从而产生大规模的数据交换动作  
因为产生了数据交换，当前的数据流水线(Stage)也将被截断，在数据重新分配之后，开始一个新的数据流水线(Stage)，故而每遇到一个Shuffle算子，都会产生一个新的Stage
常见的宽依赖算子有 groupByKey, repartition 等

## 创建 RDD
创建RDD的方式主要有两种：通过并行化现有的集合创建RDD；或者通过读取外部系统如HDFS等创建RDD  
本篇文章的后续实践可在 spark-shell 中完成, 其中会默认实例化一个 SparkContext 实例 `sc` 和 SparkSession 实例 `spark`
```shell
spark-shell
```
### 并行化现有集合 
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

### 读取外部系统数据   
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

## Transformation 算子
### 基础转换
#### map
```
scala> val intRDD = sc.range(0, 5)
intRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[0] at range at <console>:23
scala>  val transformedRDD = intRDD.map(_ * 2)
transformedRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[1] at map at <console>:23cala> val transformedRDD = intRDD
scala> transformedRDD.collect
res0: Array[Long] = Array(0, 2, 4, 6, 8)
```
#### filter
```
scala> val intRDD = sc.range(0, 5)
intRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[0] at range at <console>:23
scala>  val filteredRDD = intRDD.filter(_ <= 2)
filteredRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[1] at filter at <console>:23
scala> filteredRDD.collect
res0: Array[Long] = Array(0, 1, 2)
```
#### flatMap
```
scala> val twoDList = List(List(1, 2), List(3, 4))
twoDList: List[List[Int]] = List(List(1, 2), List(3, 4))
scala> val rddFromCollection= sc.parallelize(twoDList)
rddFromCollection: org.apache.spark.rdd.RDD[List[Int]] = ParallelCollectionRDD[0] at parallelize at <console>:24cala> val rddFromCollection= sc.parallelize(twoDList)
scala> val transformedDF = rddFromCollection.flatMap(l => l.map(_ * 2))
transformedDF: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[1] at flatMap at <console>:23
scala> transformedDF.collect
res0: Array[Int] = Array(2, 4, 6, 8)
```
#### sample
```
scala> val rddFromCollection = sc.parallelize(1 to 100)
rddFromCollection: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23
scala> val sampleRDD = rddFromCollection.sample(true, 0.1)
sampleRDD: org.apache.spark.rdd.RDD[Int] = PartitionwiseSampledRDD[1] at sample at <console>:23
scala> sampleRDD.collect
res0: Array[Int] = Array(15, 17, 21, 21, 36, 43, 54, 59, 63, 67, 83, 83, 95)
```
#### pipe
```
scala>  val rddFromCollection = sc.parallelize(1 to 100)
rddFromCollection: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23
scala> rddFromCollection.pipe("grep 0").collect
res0: Array[String] = Array(10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
```

### 分区转换
#### mapPartitions
#### mapPartitionsWithIndex
#### coalesce
#### repartition
#### repartitionAndSortWithinPartitions

### 集合运算
#### union
#### intersection
#### join
#### cogroup
zipWithKey
#### cartesian
cross join

### 聚合操作
#### groupByKey
#### reduceByKey
#### aggregateByKey

### 其他
#### sortByKey
#### distinct


## Action 算子
### 转换为内存集合
#### reduce
#### collect
#### count
#### first
#### take
#### takeSample
#### takeOrdered
#### countByKey

### 写入外部系统
#### saveAsTextFile
#### saveAsSequenceFile
#### saveAsObjectFile
#### foreach

## Control 算子
### persist
### checkpoint

## 全局变量
### Broadcast
### Accumulators
