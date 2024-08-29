# Spark RDD - Action 算子
## 转换为内存集合
### reduce
对 RDD 进行 reduce 操作, 所有记录按照用户指定的 (left, right) => result 函数从左到右进行合并, 返回一个 Java 集合
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.reduce(_ + _)
res0: Int = 21
```
### treeReduce 
语义上与 [reduce](#reduce) 等价 ，只是在合并结果时，treeAggregate 将以多级树的形式逐级聚合，降低 Driver 端的压力  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.treeReduce(_ + _, depth=2)
res0: Int = 21
```
### fold
对 RDD 进行合并操作, 所有记录按照用户指定的 (left, right) => result 函数从左到右进行合并, 返回一个 Java 集合  
与 [reduce](#reduce) 的功能很相似，不同的是 fold 允许用户提供一个作用于每个分区的初始值
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.fold(0)(_ + _)
res0: Int = 21
```
### aggregate
对 RDD 进行聚合操作，与 [aggregateByKey](#aggregateByKey) 算子类似，只是面向 RDD 的所有记录，而非以 Key 为单位。  
操作分两个阶段，先对单个分区内的数据聚合，再对所有分区聚合结果进行聚合，从而得到最终的聚合结果,
它允许返回一个与 RDD 记录类型 V 不同的类型 U, 比如将元素(Int) group 成一个 List  
因此需要指定一个初始值，和两个聚合函数  
- zeroValue: U, 作用在每个分区的初始值  
- seqOp: (U, V) => U, 作用在每个分区内数据的聚合函数  
- combOp: (U, U) => U, 作用在每个分区聚合结果上的聚合函数   
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.aggregate(0)(_+_, _+_)
res0: Int = 21
```
### treeAggregate
语义上与 [aggregate](#aggregate) 等价，只是在合并分区结果时，treeAggregate 将以多级树的形式逐级聚合，降低 Driver 端的压力   
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.treeAggregate(0)(_+_, _+_, depth=2)
res0: Int = 21
```
### collect
将 RDD 的所有记录收集起来，返回一个 Java 的 Array 集合到 Driver 端  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.treeAggregate(0)(_+_, _+_, depth=2)
res0: Array[Int] = Array(1, 2, 3, 4, 5, 6)
```
### collectAsMap
将 K-V Pair 型 RDD 的所有记录起来，返回一个 Java 的 Map 集合到 Driver 端   
***只能作用于 K-V Pair 型 RDD***
``` 
scala> val rdd = sc.parallelize(List("A" -> 1, "B" -> 2))
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.collectAsMap
res0: scala.collection.Map[String,Int] = Map(A -> 1, B -> 2)
```
### count
返回 RDD 的总记录数
```
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.count
res0: Long = 6
```
### countByKey
返回 K-V Pair 型 RDD 的每个 Key 的记录数  
***只能作用于 K-V Pair 型 RDD***
```
scala> val rdd = sc.parallelize(List("A" -> 1, "A" -> 11, "B" -> 2))
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.countByKey
res0: scala.collection.Map[String,Long] = Map(B -> 1, A -> 2)

```
### countApprox
返回 RDD 总记录数的近似值, 在给定的 timeout 时间内返回有 confidence 概率准确的记录数的区间  
``` 
scala> val rdd = sc.parallelize(1 to 10000 * 10000, 1000)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.countApprox(timeout=500, confidence=0.95)
res0: org.apache.spark.partial.PartialResult[org.apache.spark.partial.BoundedDouble] = (partial: [99984958.000, 100015042.000])

scala> rdd.countApprox(timeout=500, confidence=0.0)
res126: org.apache.spark.partial.PartialResult[org.apache.spark.partial.BoundedDouble] = (partial: [100000000.000, 100000000.000]
```
### countByKeyApprox
返回 K-V Pair 型 RDD 的每个 Key 的记录数的近似值, 在给定的 timeout 时间内返回各个 Key 有 confidence 概率准确的记录数的区间  
***只能作用于 K-V Pair 型 RDD***
``` 
scala> val rdd = sc.parallelize(List("A", "B", "C"), 1) cartesian sc.parallelize(1 to 10000 * 10000, 100)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.countByKeyApprox(timeout=5000, confidence=0.95)
res0: org.apache.spark.partial.PartialResult[scala.collection.Map[String,org.apache.spark.partial.BoundedDouble]] = (partial: Map(B -> [99990807.000, 100009194.000], A -> [99990807.000, 100009194.000], C -> [99990807.000, 100009194.000]))

scala> rdd.countByKeyApprox(timeout=5000, confidence=0.0)
res1: org.apache.spark.partial.PartialResult[scala.collection.Map[String,org.apache.spark.partial.BoundedDouble]] = (partial: Map(B -> [100000000.000, 100000000.000], A -> [100000000.000, 100000000.000], C -> [100000000.000, 100000000.000]))
```

### countByValue
返回 RDD 中每条记录出现的次数  
``` 
scala> val rdd = sc.parallelize(List("A", "A", "B", "B", "C"))
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:25

scala> rdd.countByValue
res0: scala.collection.Map[String,Long] = Map(B -> 2, C -> 1, A -> 2)
```
### countByValueApprox 
返回 RDD 中每条记录出现的次数的近似值, 在给定的 timeout 时间内返回各个 Key 有 confidence 概率准确的记录数的区间
``` 
scala> val rdd = sc.parallelize(1 to 3000 * 10000, 100).map(_ % 3)
rdd: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[281] at map at <console>:25 

scala> rdd.countByValueApprox(500, 0.95)
res0: org.apache.spark.partial.PartialResult[scala.collection.Map[Int,org.apache.spark.partial.BoundedDouble]] = (partial: Map(0 -> [9996494.000, 10003507.000], 1 -> [9996494.000, 10003507.000], 2 -> [9996494.000, 10003507.000]))

scala> rdd.countByValueApprox(500, 0.0)
res1: org.apache.spark.partial.PartialResult[scala.collection.Map[Int,org.apache.spark.partial.BoundedDouble]] = (partial: Map(0 -> [10000000.000, 10000000.000], 1 -> [10000000.000, 10000000.000], 2 -> [10000000.000, 10000000.000]))
```
### countApproxDistinct
返回 RDD 去重后的记录数的近似值, 使用的算法基于 streamlib 实现的[《HyperLogLog in practice: algorithmic engineering of a state of the art cardinality estimation algorithm》](https://dl.acm.org/doi/10.1145/2452376.2452456)  
p：正常集合的精度值  
sp：稀疏集合的精度值  
``` 
scala> val rdd = sc.parallelize(1 to 10000 * 10000, 100).map(_ % 1000)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.distinct.count
res0: Long = 3

scala> rdd.countApproxDistinct(4, 0)
res1: Long = 1213

```
### max
返回 RDD 中记录的最大值  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.max
res0: Int = 6
```
### min
返回 RDD 中记录的最大值
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.min
res0: Int = 1
```
### isEmpty
判断 RDD 是否为空, 返回 true 或 false  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.isEmpty
res0: Boolean = false
```
### first
返回 RDD 的第一条记录  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.first
res0: Int = 1
```
### take
返回 RDD 中的 n 条记录, 默认先从一个 partition 中获取，不足 n 时再从其他 partition 中获取, 直到满足 n 为止
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.take(3)
res0: Array[Int] = Array(1, 2, 3)
```
### top
返回 RDD 降序排序之后的前 n 条记录，与 [takeOrdered](#takeordered) 相反
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.top(3)
res0: Array[Int] = Array(6, 5, 4)
```
### takeOrdered
返回 RDD 升序排序之后的前 n 条记录, 与 [top](#top) 相反
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.takeOrdered(3)
res0: Array[Int] = Array(1, 2, 3)
```
### takeSample
返回 RDD 中随机的 n 条记录
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala>  rdd.takeSample(withReplacement=false, 3)
res0: Array[Int] = Array(2, 1, 6)
```
### foreach
遍历 RDD 中的每一条记录，根据提供的 record => Unit 函数，将记录写入外部系统，或打印到控制台，或添加到其他 Java 集合中等
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.foreach(x => print(x + ","))
4,1,6,5,2,3,
```

## 写入外部系统
### saveAsTextFile
将 RDD 以 TEXT 文件格式写入 Hadoop 支持的外部文件系统
### saveAsSequenceFile
将 RDD 以 Hadoop SequenceFile 文件格式写入 Hadoop 支持的外部文件系统
### saveAsObjectFile
将 RDD 序列化之后， 以 Hadoop SequenceFile 文件格式写入 Hadoop 支持的外部文件系统
### saveAsHadoopFile
等效于 [saveAsTextFile](#saveAsTextFile)
### saveAsNewAPIHadoopFile
将 K-V Pair 型 RDD，以指定的文件格式写入 Hadoop 支持的外部文件系统
### saveAsHadoopDataset 
将 K-V Pair 型 RDD，以指定的文件格式写入 Hadoop 支持的外部存储系统中(如 HDFS、HBase等)
