# Spark RDD
## RDD 简介
RDD(Resilient Distributed Dataset) - 弹性分布式数据集，是 Spark 用来并行操作跨节点数据的主要抽象。
### RDD的五大特性
1. 一组分区：每个RDD拥有一组partitions, 每个partition将由一个task来处理；
2. 数据血缘：每个RDD记录了其依赖关系，可向上追溯父RDD，发生错误时，可从父RDD开始重新计算；
3. 转换函数：每个RDD拥有其转换函数，记录了其是怎样通过父RDD转换而来的；
4. 分区器：每个RDD拥有一个Partitioner, 记录了其重新分区的规则；
5. 数据本地性：移动计算优于移动数据，RDD会尽可能让计算task发生在离数据更近的地方。
### Shuffle 操作
Shuffle 是 Spark 进行数据交换或者说重新分配数据的一种操作，这通常会产生跨 Executor 、跨节点，甚至跨机房、跨地区的数据拷贝，因此 Shuffle 操作的成本一来说都比较高。  
只有宽依赖(Wide-Dependency)算子会产生Shuffle, 窄依赖(Narrow-Dependency)算子不会产生Shuffle。    

![image](https://github.com/tangchenyang/picx-images-hosting/raw/master/20240808/image.5c0w5b3q3u.webp)   

#### 窄依赖  
父RDD的每一个分区，最多只会被子RDD的一个分区所依赖，这意味着在计算过程中，当前partition中的数据，不需要与其他partitions中的数据进行交互，即可完成计算。  
因为不涉及Shuffle，这类算的的计算速度一般都很快；也以为其一对一的特点，多个相邻的窄依赖算子可以被Chain起来，放在一个Stage中，形成一个优化的流水线。
常见的窄依赖算子有 map, filter, union 等。
#### 宽依赖
父RDD的每一个分区，会被自RDD的多个分区所依赖, 这意味着当前partition中的数据，会按需(partitioner)被重新分配到子RDD的不同各个partition中，从而产生大规模的数据交换动作。  
因为产生了数据交换，当前的数据流水线(Stage)也将被截断，在数据重新分配之后，开始一个新的数据流水线(Stage)，故而每遇到一个Shuffle算子，都会产生一个新的Stage。
常见的宽依赖算子有 groupByKey, repartition 等。

## 创建 RDD
创建RDD的方式主要有两种：通过并行化现有的集合创建 RDD ；或者通过读取外部系统如 HDFS 等创建 RDD。  
本篇文章的后续实践可在 spark-shell 中完成, 其中会默认实例化一个 SparkContext 实例 `sc` 和 SparkSession 实例 `spark`。
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
对RDD的每一条记录做转换操作
```
scala> val intRDD = sc.range(0, 5)
intRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[0] at range at <console>:23

scala>  val transformedRDD = intRDD.map(_ * 2)
transformedRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[1] at map at <console>:23cala> val transformedRDD = intRDD

scala> transformedRDD.collect
res0: Array[Long] = Array(0, 2, 4, 6, 8)
```
#### filter
对RDD的每一条记录做过滤操作
```
scala> val intRDD = sc.range(0, 5)
intRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[0] at range at <console>:23

scala>  val filteredRDD = intRDD.filter(_ <= 2)
filteredRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[1] at filter at <console>:23

scala> filteredRDD.collect
res0: Array[Long] = Array(0, 1, 2)
```
#### flatMap
对RDD的每一条记录中的集合列做转换操作，同时将数组中的元素展开成多行
```
scala> val twoDList = List(List(1, 2), List(3, 4))
twoDList: List[List[Int]] = List(List(1, 2), List(3, 4))

scala> val rdd= sc.parallelize(twoDList)
rdd: org.apache.spark.rdd.RDD[List[Int]] = ParallelCollectionRDD[0] at parallelize at <console>:24cala> val rdd= sc.parallelize(twoDList)

scala> val transformedDF = rdd.flatMap(l => l.map(_ * 2))
transformedDF: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[1] at flatMap at <console>:23

scala> transformedDF.collect
res0: Array[Int] = Array(2, 4, 6, 8)
```
#### sample
对RDD进行采样，返回样本记录, fraction 不代表精确的比例，仅代表每条记录被命中的概率
```
scala> val rdd = sc.parallelize(1 to 100)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val sampleRDD = rdd.sample(withReplacement=true, fraction=0.1)
sampleRDD: org.apache.spark.rdd.RDD[Int] = PartitionwiseSampledRDD[1] at sample at <console>:23

scala> sampleRDD.collect
res0: Array[Int] = Array(15, 17, 21, 21, 36, 43, 54, 59, 63, 67, 83, 83, 95)
```
#### sampleByKey
对 K-V Pair 型 RDD 进行采样，返回每个 Key 的样本记录, fraction 不代表精确的比例，仅代表各个 Key 的每条记录被命中的概率
***只能作用于 K-V Pair 型 RDD***
``` 
scala> val rdd = sc.parallelize(List("A", "B", "C")).cartesian(sc.parallelize(1 to 100))
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val sampleRDD = rdd.sampleByKey(withReplacement=false, Map("A" -> 0.05, "B" -> 0.05, "C" -> 0.1))
kvRDD: org.apache.spark.rdd.RDD[(Int, Int)] = MapPartitionsRDD[1] at keyBy at <console>:24

scala> sampleRDD.collect
res0: Array[(String, Int)] = Array((A,63), (A,65), (A,68), (A,82), (B,25), (B,85), (B,100), (C,5), (C,8), (C,10), (C,18), (C,27), (C,38), (C,82), (C,96))
```
#### pipe
对RDD进行操作系统级的管道操作
```
scala> val rdd = sc.parallelize(1 to 100)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.pipe("grep 0").collect
res0: Array[String] = Array(10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
```
#### zipWithIndex
为RDD的每一条记录生成Index, 返回 (record, index) 的元祖  
其 Index 是根据每个 partition 的 Index 和各个 partition 中每个元素的 index 计算而来，因此产生一个额外的 Job
```
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val zippedRDD = rdd.zipWithIndex
zippedRDD: org.apache.spark.rdd.RDD[(Int, Long)] = ZippedWithIndexRDD[1] at zipWithIndex at <console>:23

scala> zippedRDD.collect
res0: Array[(Int, Long)] = Array((1,0), (2,1), (3,2), (4,3), (5,4), (6,5))
```

#### zipWithUniqueId
为RDD的每一条记录生成唯一ID, 返回 (record, uniqueId) 的元祖  
其 uniqueId 是根据 UID = itemIndex * partitionNum + partitionIndex 生成的, 因此不同于 zipWithIndex, 此算子不会产生额外的 Job
```
scala> val rdd = sc.parallelize(1 to 6, 2)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val zippedRDD = rdd.zipWithUniqueId
zippedRDD: org.apache.spark.rdd.RDD[(Int, Long)] = MapPartitionsRDD[1] at zipWithUniqueId at <console>:23

scala> zippedRDD.collect
res0: Array[(Int, Long)] = Array((1,0), (2,2), (3,4), (4,1), (5,3), (6,5))
```
#### sortBy
对 RDD 进行排序，将以用户指定的 U => V 函数的返回值作为排序依据  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala>  val descSortedRDD = rdd.sortBy(x => x, ascending=false)
sortedRDD: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[1] at sortBy at <console>:23

scala> descSortedRDD.collect
res0: Array[Int] = Array(6, 5, 4, 3, 2, 1)
```
#### sortByKey
对 K-V Pair 型 RDD 按 Key 进行排序  
***只能作用于 K-V Pair 型 RDD***
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val kvRDD = rdd.keyBy(x => x)
sortedRDD: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[1] at sortBy at <console>:23

scala>  val ascSortedRDD = kvRDD.sortByKey(ascending=true)
ascSortedRDD: org.apache.spark.rdd.RDD[(Int, Int)] = ShuffledRDD[2] at sortByKey at <console>:23

scala> ascSortedRDD.collect
res0: Array[(Int, Int)] = Array((1,1), (2,2), (3,3), (4,4), (5,5), (6,6))
```
#### distinct
对 RDD 进行去重, 完全相同的记录将被移除  
``` 
scala> val rdd = sc.parallelize(List("A" -> 1, "A" -> 1, "A" -> 11, "B" -> 2))
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val distinctedRDD = rdd.distinct
distinctedRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[1] at distinct at <console>:23

scala> distinctedRDD.collect
res0: Array[(String, Int)] = Array((A,1), (B,2), (A,11))
```

#### keyBy
为RDD的每一条记录生成一个 Key, 返回(key, record) 的元祖，key 由用户指定的 record => key 函数生成
```
scala> val rdd = sc.parallelize(1 to 6, 2)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedDF = rdd.keyBy { x => if (x % 2 == 0) "even" else "odd" }
transformedDF: org.apache.spark.rdd.RDD[(Int, Int)] = MapPartitionsRDD[1] at keyBy at <console>:23

scala> transformedDF.collect
res0: Array[(String, Int)] = Array((odd,1), (even,2), (odd,3), (even,4), (odd,5), (even,6))
```
#### mapValues
对 K-V Pair 型 RDD 的每一条记录的 values 进行转换  
***只能作用于 K-V Pair 型 RDD***
```
scala> val rdd = sc.parallelize(List("A" -> 1, "B" -> 2))
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rdd.mapValues(_ * 2)
transformedRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[1] at mapValues at <console>:23

scala> transformedRDD.collect
res0: Array[(String, Int)] = Array((A,2), (B,4))
```
#### flatMapValues
对 K-V Pair 型 RDD的每一条记录中的集合列做转换操作，同时将数组中的元素展开成多行  
***只能作用于 K-V Pair 型 RDD***  
``` 
scala> val rdd = sc.parallelize(List(1 -> List("A", "a"), 2 -> List("B", "b")))
rdd: org.apache.spark.rdd.RDD[(Int, List[String])] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rdd.flatMapValues(l => l.map(_ * 2))
transformedRDD: org.apache.spark.rdd.RDD[(Int, String)] = MapPartitionsRDD[1] at flatMapValues at <console>:23

scala> transformedRDD.collect
res0: Array[(Int, String)] = Array((1,AA), (1,aa), (2,BB), (2,bb))
```


### 分区转换
#### mapPartitions
对 RDD 的每一个分区做转换操作，每个分区中的元素被封装成一个迭代器，因此这个转换函数应是 iterator => iterator 的映射
```
scala> val rdd = sc.parallelize((1 to 6).map(_.toString), 3)
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rdd.mapPartitions{ iter => val salt = "abcd_"; iter.map(x=>salt + x) }
transformedRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[1] at mapPartitions at <console>:24

scala> transformedRDD.collect
res0: Array[String] = Array(abcd_1, abcd_2, abcd_3, abcd_4, abcd_5, abcd_6)
```
#### mapPartitionsWithIndex
对 RDD 的每一个分区做转换操作，每个分区中的元素被封装成一个迭代器, 并拥有当前 partition 的 Index，因此这个转换函数应是 (partitionIndex, iterator) => iterator 的映射
```
scala> val rdd = sc.parallelize((1 to 6).map(_.toString), 3)
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rdd.mapPartitionsWithIndex{(idx, iter) => iter.map(x=> s"p_${idx}__${x}")}
transformedRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[1] at mapPartitionsWithIndex at <console>:23

scala> transformedRDD.collect
res0: Array[String] = Array(p_0__1, p_0__2, p_1__3, p_1__4, p_2__5, p_2__6)
```
#### glom 
将 RDD 的每个分区中的所有记录合并成一个 Array
```
scala> val rdd = sc.parallelize((1 to 6).map(_.toString), 3)
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rdd.glom
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> transformedRDD.collect
res0: Array[Array[String]] = Array(Array(1, 2), Array(3, 4), Array(5, 6))
```
#### zipPartitions
将两个RDD按分区进行 zip, 并按用户给定的 (Iter[A], Iter[B]) => Iter[C] 函数，在每个 partition 中返回新的迭代器
```
scala> val rdd1 = sc.parallelize(1 to 4, 2)
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(List("A", "B", "C", "D"), 2)
rdd2: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val zippedRDD = rdd1.zipPartitions(rdd2)((iter1, iter2) => iter1 zip iter2)
zippedRDD: org.apache.spark.rdd.RDD[(Int, String)] = ZippedPartitionsRDD2[2] at zipPartitions at <console>:24

scala> zippedRDD.collect
res0: Array[(Int, String)] = Array((1,A), (2,B), (3,C), (4,D))
```
#### coalesce
减少 RDD 的分区，默认不产生 Shuffle, 当目标分区数大于当前分区数时，将保持当前分区数 
也可将 shuffle 设置为 true，以得到更多的分区，但是会产生Shuffle, 此场景建议使用 repartition 
``` 
scala> val rdd = sc.parallelize((1 to 6).map(_.toString), 3)
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[34] at parallelize at <console>:23

scala> rdd.coalesce(2).partitions.size
res0: Int = 2

scala> rdd.coalesce(10).partitions.size
res1: Int = 3

scala> rdd.coalesce(10, shuffle=true).partitions.size
res2: Int = 10
```
#### repartition
调整 RDD 的分区到目标数量，对数据进行随机重新分布，会产生 Shuffle  
```
scala> val rdd = sc.parallelize(-5 to 10, 2)
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val repartitionedRDD = rdd.repartition(3)
repartitionedRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[65] at repartition at <console>:23

scala> repartitionedRDD.partitions.size
res0: Int = 3

scala> repartitionedRDD.mapPartitions(iter => Iterator(iter.toList)).collect
res1: Array[List[String]] = Array(List(-5, -2, 1, 5, 8), List(-4, -1, 2, 3, 6, 9), List(-3, 0, 4, 7, 10))
```
#### partitionBy
调整 K-V Pair 型 RDD 的分区到目标数量，根据 Key 值对数据进行重新分布，会产生 Shuffle  
***只能作用于 K-V Pair 型 RDD***
```
scala> val rdd = sc.parallelize(-5 to 10, 2)
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val kvRDD = rdd.keyBy { x => if (x < 0) "negative number" else "non-negative number" }

scala> val repartitionedRDD = kvRDD.partitionBy(new org.apache.spark.HashPartitioner(3))
repartitionedRDD: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[] at partitionBy at <console>:24

scala> repartitionedRDD.partitions.size
res0: Int = 3

scala> repartitionedRDD.values.mapPartitions(iter => Iterator(iter.toList)).collect
res1: Array[List[Int]] = Array(List(), List(-5, -4, -3, -2, -1), List(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
```

### 集合运算
#### union
对两个RDD求并集
```
scala> val rdd1 = sc.parallelize(1 to 5, 2)
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(6 to 10, 2)
rdd2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val unionRDD = rdd1.union(rdd2)
unionRDD: org.apache.spark.rdd.RDD[Int] = UnionRDD[2] at union at <console>:24

scala> unionRDD.collect
res0: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
```
#### intersection
对两个RDD求交集
``` 
scala> val rdd1 = sc.parallelize(1 to 5, 2)
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(3 to 7, 2)
rdd2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val intersectionRDD = rdd1.intersection(rdd2)
unionRDD: org.apache.spark.rdd.RDD[Int] = UnionRDD[2] at union at <console>:24

scala> intersectionRDD.collect
res0: Array[Int] = Array(4, 3, 5)
```
#### subtract
对RDD求差集, 返回在 rdd1 但不在 rdd2 中的记录
```
scala> val rdd1 = sc.parallelize(1 to 5)
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(3 to 7)
rdd2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val subtractRDD = rdd1.subtract(rdd2)
unionRDD: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[129] at subtract at <console>:24

scala> subtractRDD.collect
res0: Array[Int] = Array(1, 2)
```
#### join
将两个RDD 按 Key 关联在一起，返回关联后的RDD, 对于重复 value，会单独出现在不同记录中  
***只能作用于 K-V Pair 型 RDD***  
``` 
scala> val rdd1 = sc.parallelize(List(1 -> "a", 2 -> "b"))
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(List(1 -> "A", 2 -> "B", 2 -> "Bb"))
rdd2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val joinedRDD = rdd1.join(rdd2)
joinedRDD: org.apache.spark.rdd.RDD[(Int, (String, String))] = MapPartitionsRDD[30] at join at <console>:24

scala> joinedRDD.collect
res0: Array[(Int, (String, String))] = Array((1,(a,A)), (2,(b,B)), (2,(b,Bb)))
```
#### cogroup
将两个RDD按 Key 关联在一起，返回关联后的RDD，相同 Key 的 value 会被 group 到一个集合中  
***只能作用于 K-V Pair 型 RDD***
``` 
scala> val rdd1 = sc.parallelize(List(1 -> "a", 2 -> "b"))
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(List(1 -> "A", 2 -> "B", 2 -> "Bb"))
rdd2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val cogroupedRDD = rdd1.cogroup(rdd2)
cogroupedRDD: org.apache.spark.rdd.RDD[(Int, (Iterable[String], Iterable[String]))] = MapPartitionsRDD[3 at cogroup at <console>:24

scala> cogroupedRDD.collect
res0: Array[(Int, (Iterable[String], Iterable[String]))] = Array((1,(CompactBuffer(a),CompactBuffer(A))), (2,(CompactBuffer(b),CompactBuffer(B, Bb))))
```
#### groupWith
[cogroup](#cogroup) 的别名，行为与 cogroup 完全一致
#### leftOuterJoin
将当前 RDD 与另外的 RDD 进行左关联, 结果集中仅包含左 RDD 中的全部记录，右 RDD 中匹配不到的数据置为空  
即对于每一条记录 (key, value_left), 能匹配到时返回 (key, (value_left, value_right)), 匹配不到时返回(key, (value_left, None))  
***只能作用于 K-V Pair 型 RDD***  
```
scala> val rdd1 = sc.parallelize(List(1 -> "a", 2 -> "b", 3 -> "c"))
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(List(1 -> "A", 2 -> "B", 2 -> "Bb", 4 -> "D"))
rdd2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val leftJoinedRDD = rdd1.leftOuterJoin(rdd2)
leftJoinedRDD: org.apache.spark.rdd.RDD[(Int, (String, Option[String]))] = MapPartitionsRDD[4] at leftOuterJoin at <console>:24

scala> leftJoinedRDD.collect
res0: Array[(Int, (String, Option[String]))] = Array((1,(a,Some(A))), (2,(b,Some(B))), (2,(b,Some(Bb))), (3,(c,None)))
```
#### rightOuterJoin
将当前 RDD 与另外的 RDD 进行右关联, 结果集中仅包含右 RDD 中的全部记录，左 RDD 中匹配不到的数据置为空  
即对于每一条记录 (key, value_left), 能匹配到时返回 (key, (value_left, value_right)), 匹配不到时返回(key, (None, value_right))  
***只能作用于 K-V Pair 型 RDD***  
``` 
scala> val rdd1 = sc.parallelize(List(1 -> "a", 2 -> "b", 3 -> "c"))
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(List(1 -> "A", 2 -> "B", 2 -> "Bb", 4 -> "D"))
rdd2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val rightJoinedRDD = rdd1.rightOuterJoin(rdd2)
leftJoinedRDD: org.apache.spark.rdd.RDD[(Int, (String, Option[String]))] = MapPartitionsRDD[4] at leftOuterJoin at <console>:24

scala> rightJoinedRDD.collect
res0: Array[(Int, (Option[String], String))] = Array((1,(Some(a),A)), (2,(Some(b),B)), (2,(Some(b),Bb)), (4,(None,D)))
```
#### fullOuterJoin
将当前 RDD 与另外的 RDD 进行全关联, 结果集中将包含左右 RDD 中的全部记录，匹配不到的数据置为空
即对于每一条记录 (key, value_left), 能匹配到时返回 (key, (value_left, value_right)), 匹配不到时返回(key, (value_left, value_right)) 或 (key, (None, value_right))  
***只能作用于 K-V Pair 型 RDD***  
``` 
scala> val rdd1 = sc.parallelize(List(1 -> "a", 2 -> "b", 3 -> "c"))
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(List(1 -> "A", 2 -> "B", 2 -> "Bb", 4 -> "D"))
rdd2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val fullJoinedRDD = rdd1.fullOuterJoin(rdd2)
leftJoinedRDD: org.apache.spark.rdd.RDD[(Int, (String, Option[String]))] = MapPartitionsRDD[4] at leftOuterJoin at <console>:24

scala> fullJoinedRDD.collect
res0: Array[(Int, (Option[String], Option[String]))] = Array((1,(Some(a),Some(A))), (2,(Some(b),Some(B))), (2,(Some(b),Some(Bb))), (3,(Some(c),None)), (4,(None,Some(D))))
```
#### subtractByKey
对 K-V Pair 型 RDD 求差集, 返回 key 在 rdd1 但不在 rdd2 中的记录  
***只能作用于 K-V Pair 型 RDD***
```
scala> val rdd1 = sc.parallelize(List(1 -> "a", 2 -> "b", 3 -> "c"))
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(List(1 -> "A", 2 -> "B", 2 -> "Bb", 4 -> "D"))
rdd2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val subtractedRDD = rdd1.subtractByKey(rdd2)
subtractedRDD: org.apache.spark.rdd.RDD[(Int, String)] = SubtractedRDD[2] at subtractByKey at <console>:24

scala> subtractedRDD.collect
res0: Array[(Int, String)] = Array((3,c))
```
#### cartesian
对两个RDD进行笛卡尔积运算
``` 
scala> val rdd1 = sc.parallelize(1 to 3)
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(List( "A", "B", "C"))
rdd2: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val cartesianRDD = rdd1.cartesian(rdd2)
cartesianRDD: org.apache.spark.rdd.RDD[(Int, String)] = CartesianRDD[2] at cartesian at <console>:24

scala> cartesianRDD.collect
res0: Array[(Int, String)] = Array((1,A), (1,B), (1,C), (2,A), (2,B), (2,C), (3,A), (3,B), (3,C))
```
#### randomSplit
将RDD切分成一组RDD, 切分成多少组由权重 weights 的数组大小决定, 权重不代表精确的比例，仅代表每条记录被命中的概率
```
scala> val rdd = sc.parallelize(1 to 10)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val splitedRDDs = rdd.randomSplit(Array(0.2, 0.2, 0.6))
splitedRDDs: Array[org.apache.spark.rdd.RDD[Int]] = Array(MapPartitionsRDD[1] at randomSplit at <console>:23, MapPartitionsRDD[98] at randomSplit at <console>:23, MapPartitionsRDD[99] at randomSplit at <console>:23)

scala> splitedRDDs.map(_.collect)
res0: Array[Array[Int]] = Array(Array(2, 3, 6), Array(5, 7, 9), Array(1, 4, 8, 10))
```
#### zip
将两个RDD按index进行zip, 返回具有相同 index 的 (record1, record2) 的元祖 
```
scala> val rdd1 = sc.parallelize(1 to 4, 2)
rdd1: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2 = sc.parallelize(List("A", "B", "C", "D"), 2)
rdd2: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val zippedRDD = rdd1.zip(rdd2)
zippedRDD: org.apache.spark.rdd.RDD[(Int, String)] = ZippedPartitionsRDD2[2] at zipPartitions at <console>:24

scala> zippedRDD.collect
res0: Array[(Int, String)] = Array((1,A), (2,B), (3,C), (4,D))
```


### 聚合操作
#### groupBy
对 RDD 按 key 进行分组, 具有相同 key 的记录会被 group 到一起, key 值由用户指定的 record => key 函数决定
```
scala> val rdd = sc.parallelize(1 to 6, 2)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val groupedRDD = rdd.groupBy { x => if (x % 2 == 0) "even" else "odd" }
transformedDF: org.apache.spark.rdd.RDD[(Int, Int)] = MapPartitionsRDD[1] at keyBy at <console>:23

scala> groupedRDD.collect
res0: Array[(String, Iterable[Int])] = Array((even,CompactBuffer(2, 4, 6)), (odd,CompactBuffer(1, 3, 5)))
```
#### groupByKey
对 K-V Pair 型 RDD 按 key 进行分组, 具有相同 key 的记录会被 group 到一起  
***只能作用于 K-V Pair 型 RDD***
```
scala> val rdd = sc.parallelize(1 to 6, 2)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val kvRDD = rdd.keyBy { x => if (x % 2 == 0) "even" else "odd" }
kvRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[1] at keyBy at <console>:23

scala> val groupedRDD = kvRDD.groupByKey()
groupedRDD: org.apache.spark.rdd.RDD[(String, Iterable[Int])] = ShuffledRDD[2] at groupByKey at <console>:23

scala> groupedRDD.collect
res0: Array[(String, Iterable[Int])] = Array((even,CompactBuffer(2, 4, 6)), (odd,CompactBuffer(1, 3, 5)))
```
#### reduceByKey
对 K-V Pair 型 RDD 按 key 进行 reduce 操作, 具有相同 key 的记录将按照用户指定的 (left, right) => result 函数从左到右进行合并  
***只能作用于 K-V Pair 型 RDD***
```
scala> val rdd = sc.parallelize(1 to 6, 2)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val kvRDD = rdd.keyBy { x => if (x % 2 == 0) "even" else "odd" }
kvRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[1] at keyBy at <console>:23

scala> val reducedRDD = kvRDD.reduceByKey(_ + _)
reducedRDD: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[2] at reduceByKey at <console>:23

scala> reducedRDD.collect
res0: Array[(String, Int)] = Array((even,12), (odd,9))
```
#### foldByKey
对 K-V Pair 型 RDD 按 key 进行合并, 具有相同 key 的记录将按照用户指定的 (left, right) => result 函数从左到右进行合并  
与 [reduceByKey](#reduceByKey) 的功能很相似，不同的是 foldByKey 允许用户提供一个作用于每个分区的初始值  
***只能作用于 K-V Pair 型 RDD***
```
scala> val rdd = sc.parallelize(1 to 6, 2)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val kvRDD = rdd.keyBy { x => if (x % 2 == 0) "even" else "odd" }
kvRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[1] at keyBy at <console>:23

scala> val foldedRDD = kvRDD.foldByKey(0)(_ + _)
reducedRDD: org.apache.spark.rdd.RDD[(String, Int)] = ShuffledRDD[2] at reduceByKey at <console>:23

scala> foldedRDD.collect
res0: Array[(String, Int)] = Array((even,12), (odd,9))
```

#### aggregateByKey
对 K-V Pair 型 RDD 进行聚合操作，操作分两个阶段，先对单个分区内的数据按 Key 进行聚合，再对所有分区各个 Key 的聚合结果进行聚合，从而得到最终的聚合结果, 
它允许返回一个与 RDD 记录类型 V 不同的类型 U, 比如将元素(Int) group 成一个 List  
因此需要指定一个初始值，和两个聚合函数  
- zeroValue: U, 作用在每个分区的初始值  
- seqOp: (U, V) => U, 作用在每个分区内数据的聚合函数  
- combOp: (U, U) => U, 作用在每个分区聚合结果上的聚合函数  
***只能作用于 K-V Pair 型 RDD*** 
``` 
scala> val rdd = sc.parallelize(1 to 6, 2)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val kvRDD = rdd.keyBy { x => if (x % 2 == 0) "even" else "odd" }
kvRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[1] at keyBy at <console>:23

scala> val aggregatedRDD = kvRDD.aggregateByKey(List[Int]())(_ :+ _, _ ++ _)
aggregatedRDD: org.apache.spark.rdd.RDD[(Int, List[Int])] = ShuffledRDD[2] at aggregateByKey at <console>:23

scala> aggregatedRDD.collect
res0: Array[(String, List[Int])] = Array((even,List(2, 4, 6)), (odd,List(1, 3, 5)))
```
#### combineByKey
对 RDD 进行合并操作，与 [aggregateByKey](#aggregateByKey) 类似，操作分两个阶段，先对单个分区内的数据聚合，再对所有分区聚合结果进行聚合，从而得到最终的聚合结果,
它允许返回一个与 RDD 记录类型 V 不同的类型 U, 比如将元素(Int) group 成一个 List  
同样需要两个聚合函数，与 [aggregateByKey](#aggregateByKey) 不同的是，combineByKey 不需要指定初始值，但是需要指定一个用来创建初始值的函数, 这个函数的入参将是每个分区的第一个元素  
- createCombiner: V => U, 用于创建每个分区的初始值  
- mergeValue: (U, V) => U, 作用在每个分区内数据的聚合函数  
- mergeCombiners: (U, U) => U, 作用在每个分区聚合结果上的聚合函数   
***只能作用于 K-V Pair 型 RDD***
``` 
scala> val rdd = sc.parallelize(1 to 6, 2)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val kvRDD = rdd.keyBy { x => if (x % 2 == 0) "even" else "odd" }
kvRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[1] at keyBy at <console>:23

scala> val combinedRDD = kvRDD.combineByKey[List[Int]]((x: Int) => List[Int](x), (l: List[Int], i: Int) => l :+ i,(l1: List[Int], l2: List[Int]) => l1 ++ l2)
combinedRDD: org.apache.spark.rdd.RDD[(String, List[Int])] = ShuffledRDD[2] at combineByKey at <console>:23

scala> combinedRDD.collect
res0: Array[(String, List[Int])] = Array((even,List(2, 4, 6)), (odd,List(1, 3, 5)))
```
#### countApproxDistinctByKey
返回 K-V Pair 型 RDD 的每个 Key 去重后的记录数的近似值, 使用的算法基于 streamlib 实现的[《HyperLogLog in practice: algorithmic engineering of a state of the art cardinality estimation algorithm》](https://dl.acm.org/doi/10.1145/2452376.2452456)  
p：正常集合的精度值  
sp：稀疏集合的精度值  
***只能作用于 K-V Pair 型 RDD***
``` 
scala> val rdd = sc.parallelize(List("A", "B", "C"), 1) cartesian sc.parallelize(1 to 10000, 100).map(_ % 1000)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.distinct.countByKey
res0: scala.collection.Map[String,Long] = Map(A -> 1000, B -> 1000, C -> 1000)

scala> rdd.countApproxDistinctByKey(4, 0).collect
res1: Array[(String, Long)] = Array((A,1213), (B,1213), (C,1213))
```

## Action 算子
### 转换为内存集合
#### reduce
对 RDD 进行 reduce 操作, 所有记录按照用户指定的 (left, right) => result 函数从左到右进行合并, 返回一个 Java 集合
``` 
scala>  val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.reduce(_ + _)
res0: Int = 21
```
#### treeReduce 
语义上与 [reduce](#reduce) 等价 ，只是在合并结果时，treeAggregate 将以多级树的形式逐级聚合，降低 Driver 端的压力  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.treeReduce(_ + _, depth=2)
res0: Int = 21
```
#### fold
对 RDD 进行合并操作, 所有记录按照用户指定的 (left, right) => result 函数从左到右进行合并, 返回一个 Java 集合  
与 [reduce](#reduce) 的功能很相似，不同的是 fold 允许用户提供一个作用于每个分区的初始值
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.fold(0)(_ + _)
res0: Int = 21
```
#### aggregate
对 RDD 进行聚合操作，与 [aggregateByKey](#aggregateByKey) 算子类似，只是面向 RDD 的所有记录，而非以 Key 为单位。  
操作分两个阶段，先对单个分区内的数据聚合，再对所有分区聚合结果进行聚合，从而得到最终的聚合结果,
它允许返回一个与 RDD 记录类型 V 不同的类型 U, 比如将元素(Int) group 成一个 List  
因此需要指定一个初始值，和两个聚合函数  
- zeroValue: U, 作用在每个分区的初始值  
- seqOp: (U, V) => U, 作用在每个分区内数据的聚合函数  
- combOp: (U, U) => U, 作用在每个分区聚合结果上的聚合函数   
``` 
scala>  val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.aggregate(0)(_+_, _+_)
res0: Int = 21
```
#### treeAggregate
语义上与 [aggregate](#aggregate) 等价，只是在合并分区结果时，treeAggregate 将以多级树的形式逐级聚合，降低 Driver 端的压力   
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.treeAggregate(0)(_+_, _+_, depth=2)
res0: Int = 21
```
#### collect
将 RDD 的所有记录收集起来，返回一个 Java 的 Array 集合到 Driver 端  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.treeAggregate(0)(_+_, _+_, depth=2)
res0: Array[Int] = Array(1, 2, 3, 4, 5, 6)
```
#### collectAsMap
将 K-V Pair 型 RDD 的所有记录起来，返回一个 Java 的 Map 集合到 Driver 端   
***只能作用于 K-V Pair 型 RDD***
``` 
scala> val rdd = sc.parallelize(List("A" -> 1, "B" -> 2))
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.collectAsMap
res0: scala.collection.Map[String,Int] = Map(A -> 1, B -> 2)
```
#### count
返回 RDD 的总记录数
```
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.count
res0: Long = 6
```
#### countByKey
返回 K-V Pair 型 RDD 的每个 Key 的记录数  
***只能作用于 K-V Pair 型 RDD***
```
scala> val rdd = sc.parallelize(List("A" -> 1, "A" -> 11, "B" -> 2))
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.countByKey
res0: scala.collection.Map[String,Long] = Map(B -> 1, A -> 2)

```
#### countApprox
返回 RDD 总记录数的近似值, 在给定的 timeout 时间内返回有 confidence 概率准确的记录数的区间  
``` 
scala> val rdd = sc.parallelize(1 to 10000 * 10000, 1000)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.countApprox(timeout=500, confidence=0.95)
res0: org.apache.spark.partial.PartialResult[org.apache.spark.partial.BoundedDouble] = (partial: [99984958.000, 100015042.000])

scala> rdd.countApprox(timeout=500, confidence=0.0)
res126: org.apache.spark.partial.PartialResult[org.apache.spark.partial.BoundedDouble] = (partial: [100000000.000, 100000000.000]
```
#### countByKeyApprox
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

#### countByValue
返回 RDD 中每条记录出现的次数  
``` 
scala> val rdd = sc.parallelize(List("A", "A", "B", "B", "C"))
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:25

scala> rdd.countByValue
res0: scala.collection.Map[String,Long] = Map(B -> 2, C -> 1, A -> 2)
```
#### countByValueApprox 
返回 RDD 中每条记录出现的次数的近似值, 在给定的 timeout 时间内返回各个 Key 有 confidence 概率准确的记录数的区间
``` 
scala> val rdd = sc.parallelize(1 to 3000 * 10000, 100).map(_ % 3)
rdd: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[281] at map at <console>:25 

scala> rdd.countByValueApprox(500, 0.95)
res0: org.apache.spark.partial.PartialResult[scala.collection.Map[Int,org.apache.spark.partial.BoundedDouble]] = (partial: Map(0 -> [9996494.000, 10003507.000], 1 -> [9996494.000, 10003507.000], 2 -> [9996494.000, 10003507.000]))

scala> rdd.countByValueApprox(500, 0.0)
res1: org.apache.spark.partial.PartialResult[scala.collection.Map[Int,org.apache.spark.partial.BoundedDouble]] = (partial: Map(0 -> [10000000.000, 10000000.000], 1 -> [10000000.000, 10000000.000], 2 -> [10000000.000, 10000000.000]))
```
#### countApproxDistinct
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
#### max
返回 RDD 中记录的最大值  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.max
res0: Int = 6
```
#### min
返回 RDD 中记录的最大值
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.min
res0: Int = 1
```
#### isEmpty
判断 RDD 是否为空, 返回 true 或 false  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.isEmpty
res0: Boolean = false
```
#### first
返回 RDD 的第一条记录  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.first
res0: Int = 1
```
#### take
返回 RDD 中的 n 条记录, 默认先从一个 partition 中获取，不足 n 时再从其他 partition 中获取, 直到满足 n 为止
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.take(3)
res0: Array[Int] = Array(1, 2, 3)
```
#### top
返回 RDD 降序排序之后的前 n 条记录，与 [takeOrdered](#takeordered) 相反
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.top(3)
res0: Array[Int] = Array(6, 5, 4)
```
#### takeOrdered
返回 RDD 升序排序之后的前 n 条记录, 与 [top](#top) 相反
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.takeOrdered(3)
res0: Array[Int] = Array(1, 2, 3)
```
#### takeSample
返回 RDD 中随机的 n 条记录
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala>  rdd.takeSample(withReplacement=false, 3)
res0: Array[Int] = Array(2, 1, 6)
```
#### foreach
遍历 RDD 中的每一条记录，根据提供的 record => Unit 函数，将记录写入外部系统，或打印到控制台，或添加到其他 Java 集合中等
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.foreach(x => print(x + ","))
4,1,6,5,2,3,
```

### 写入外部系统
#### saveAsTextFile
将 RDD 以 TEXT 文件格式写入 Hadoop 支持的外部文件系统
#### saveAsSequenceFile
将 RDD 以 Hadoop SequenceFile 文件格式写入 Hadoop 支持的外部文件系统
#### saveAsObjectFile
将 RDD 序列化之后， 以 Hadoop SequenceFile 文件格式写入 Hadoop 支持的外部文件系统
#### saveAsHadoopFile
等效于 [saveAsTextFile](#saveAsTextFile)
#### saveAsNewAPIHadoopFile
将 K-V Pair 型 RDD，以指定的文件格式写入 Hadoop 支持的外部文件系统
#### saveAsHadoopDataset 
将 K-V Pair 型 RDD，以指定的文件格式写入 Hadoop 支持的外部存储系统中(如 HDFS、HBase等)


## Control 算子
### persist
将 RDD 缓存到内存或者磁盘中，通过读取缓存中的数据避免重复读取外部系统，从而提升作业性能
``` 
scala> val rddFromLocalFS = sc.textFile("file:///root/software/spark-3.5.1-bin-hadoop3/README.md")
rddFromLocalFS: org.apache.spark.rdd.RDD[String] = file:///root/software/spark-3.5.1-bin-hadoop3/README.md MapPartitionsRDD[0] at textFile at <console>:25

scala> rddFromLocalFS.persist(org.apache.spark.storage.StorageLevel.MEMORY_AND_DISK)
res0: rddFromLocalFS.type = file:///root/software/spark-3.5.1-bin-hadoop3/README.md MapPartitionsRDD[1] at textFile at <console>:25

scala> rddFromLocalFS.count
res1: Long = 125
```
### cache
等同于缓存级别为 `MEMORY_ONLY` 的 [persist](#persist)  
### unpersist
将已经缓存的 RDD 解除缓存，以释放当前作业的内存或磁盘空间  
``` 
scala> val rddFromLocalFS = sc.textFile("file:///root/software/spark-3.5.1-bin-hadoop3/README.md")
rddFromLocalFS: org.apache.spark.rdd.RDD[String] = file:///root/software/spark-3.5.1-bin-hadoop3/README.md MapPartitionsRDD[0] at textFile at <console>:25

scala> rddFromLocalFS.persist(org.apache.spark.storage.StorageLevel.MEMORY_AND_DISK)
res0: rddFromLocalFS.type = file:///root/software/spark-3.5.1-bin-hadoop3/README.md MapPartitionsRDD[1] at textFile at <console>:25

scala> rddFromLocalFS.unpersist()
```
### checkpoint
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


## 全局变量
### Broadcast
### Accumulators
