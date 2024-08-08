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

scala> val rddFromCollection= sc.parallelize(twoDList)
rddFromCollection: org.apache.spark.rdd.RDD[List[Int]] = ParallelCollectionRDD[0] at parallelize at <console>:24cala> val rddFromCollection= sc.parallelize(twoDList)

scala> val transformedDF = rddFromCollection.flatMap(l => l.map(_ * 2))
transformedDF: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[1] at flatMap at <console>:23

scala> transformedDF.collect
res0: Array[Int] = Array(2, 4, 6, 8)
```
#### sample
对RDD进行采样，返回样本记录, fraction 不代表精确的比例，仅代表每条记录被命中的概率
```
scala> val rddFromCollection = sc.parallelize(1 to 100)
rddFromCollection: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val sampleRDD = rddFromCollection.sample(true, fraction=0.1)
sampleRDD: org.apache.spark.rdd.RDD[Int] = PartitionwiseSampledRDD[1] at sample at <console>:23
scala> sampleRDD.collect

res0: Array[Int] = Array(15, 17, 21, 21, 36, 43, 54, 59, 63, 67, 83, 83, 95)
```
#### pipe
对RDD进行操作系统级的管道操作
```
scala> val rddFromCollection = sc.parallelize(1 to 100)
rddFromCollection: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rddFromCollection.pipe("grep 0").collect
res0: Array[String] = Array(10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
```
#### zipWithIndex
为RDD的每一条记录生成Index, 返回 (record, index) 的元祖  
其 Index 是根据每个 partition 的 Index 和各个 partition 中每个元素的 index 计算而来，因此产生一个额外的 Job
```
scala> val rddFromCollection = sc.parallelize(1 to 6)
rddFromCollection: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val zippedRDD = rddFromCollection.zipWithIndex
zippedRDD: org.apache.spark.rdd.RDD[(Int, Long)] = ZippedWithIndexRDD[1] at zipWithIndex at <console>:23

scala> zippedRDD.collect
res0: Array[(Int, Long)] = Array((1,0), (2,1), (3,2), (4,3), (5,4), (6,5))
```

#### zipWithUniqueId
为RDD的每一条记录生成唯一ID, 返回 (record, uniqueId) 的元祖  
其 uniqueId 是根据 UID = itemIndex * partitionNum + partitionIndex 生成的, 因此不同于 zipWithIndex, 此算子不会产生额外的 Job
```
scala> val rddFromCollection = sc.parallelize(1 to 6, 2)
rddFromCollection: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val zippedRDD = rddFromCollection.zipWithUniqueId
zippedRDD: org.apache.spark.rdd.RDD[(Int, Long)] = MapPartitionsRDD[1] at zipWithUniqueId at <console>:23

scala> zippedRDD.collect
res0: Array[(Int, Long)] = Array((1,0), (2,2), (3,4), (4,1), (5,3), (6,5))
```
#### keyBy
为RDD的每一条记录生成一个 Key, 返回(key, record) 的元祖，key 由用户指定的 record => key 函数生成
```
scala> val rddFromCollection = sc.parallelize(1 to 6, 2)
rddFromCollection: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedDF = rddFromCollection.keyBy { x => if (x % 2 == 0) "even" else "odd" }
transformedDF: org.apache.spark.rdd.RDD[(Int, Int)] = MapPartitionsRDD[1] at keyBy at <console>:23

scala> transformedDF.collect
res0: Array[(String, Int)] = Array((odd,1), (even,2), (odd,3), (even,4), (odd,5), (even,6))
```

### 分区转换
#### mapPartitions
对RDD的每一个分区做转换操作，每个分区中的元素被封装成一个迭代器，因此这个转换函数应是 迭代器 => 迭代器 的映射
```
scala> val rddFromCollection = sc.parallelize((1 to 6).map(_.toString), 3)
rddFromCollection: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rddFromCollection.mapPartitions{ iter => val salt = "abcd_"; iter.map(x=>salt + x) }
transformedRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[1] at mapPartitions at <console>:24

scala> transformedRDD.collect
res0: Array[String] = Array(abcd_1, abcd_2, abcd_3, abcd_4, abcd_5, abcd_6)
```
#### mapPartitionsWithIndex
对RDD的每一个分区做转换操作，每个分区中的元素被封装成一个迭代器, 并拥有当前 partition 的 Index，因此这个转换函数应是 (partitionIndex, 迭代器) => 迭代器 的映射
```
scala> val rddFromCollection = sc.parallelize((1 to 6).map(_.toString), 3)
rddFromCollection: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rddFromCollection.mapPartitionsWithIndex{(idx, iter) => iter.map(x=> s"p_${idx}__${x}")}
transformedRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[1] at mapPartitionsWithIndex at <console>:23

scala> transformedRDD.collect
res0: Array[String] = Array(p_0__1, p_0__2, p_1__3, p_1__4, p_2__5, p_2__6)
```
#### glom 
将RDD的每个分区中的所有记录合并成一个Array
```
scala> val rddFromCollection = sc.parallelize((1 to 6).map(_.toString), 3)
rddFromCollection: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rddFromCollection.glom
rddFromCollection: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> transformedRDD.collect
res0: Array[Array[String]] = Array(Array(1, 2), Array(3, 4), Array(5, 6))
```
#### coalesce
减少RDD的分区，默认不产生 Shuffle, 当目标分区数大于当前分区数时，将保持当前分区数 
也可将 shuffle 设置为 true，以得到更多的分区，但是会产生Shuffle, 此场景建议使用 repartition 
``` 
scala> val rddFromCollection = sc.parallelize((1 to 6).map(_.toString), 3)
rddFromCollection: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[34] at parallelize at <console>:23

scala> rddFromCollection.coalesce(2).partitions.size
res0: Int = 2

scala> rddFromCollection.coalesce(10).partitions.size
res1: Int = 3

scala> rddFromCollection.coalesce(10, shuffle=true).partitions.size
res2: Int = 10
```
#### repartition
调整RDD的分区到目标数量，会产生Shuffle，即对数据进行重新分布
```
scala> val rddFromCollection = sc.parallelize((1 to 6).map(_.toString), 3)
rddFromCollection: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[34] at parallelize at <console>:23

scala> rddFromCollection.repartitio(10).partitions.size
res0: Int = 10
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
*只能作用在 K-V Pair 型 RDD 上*  
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
*只能作用在 K-V Pair 型 RDD 上*
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
#### zipPartitions
将两个RDD按分区进行 zip, 并按用户给定的 (Iter[A], Iter[B]) => Iter[C] 返回成新的迭代器 
```
scala> val rdd1FromCollection = sc.parallelize(1 to 4, 2)
rdd1FromCollection: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val rdd2FromCollection = sc.parallelize(List("A", "B", "C", "D"), 2)
rdd2FromCollection: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> val zippedRDD = rdd1FromCollection.zipPartitions(rdd2FromCollection)((iter1, iter2) => iter1 zip iter2)
zippedRDD: org.apache.spark.rdd.RDD[(Int, String)] = ZippedPartitionsRDD2[2] at zipPartitions at <console>:24

scala> zippedRDD.collect
res0: Array[(Int, String)] = Array((1,A), (2,B), (3,C), (4,D))
```


### 聚合操作
#### aggregate
#### treeAggregate
#### groupByKey
#### reduceByKey
#### aggregateByKey

### 其他
#### sortBy
#### distinct


## Action 算子
### 转换为内存集合
#### reduce
#### collect
#### count
#### countApprox
#### countByValue
#### countByValueApprox 
#### countApproxDistinct
#### max
#### min
#### isEmpty
#### first
#### take
#### takeOrdered
#### top
#### takeSample
#### takeOrdered
#### countByKey
#### treeReduce
#### fold

### 写入外部系统
#### saveAsTextFile
#### saveAsSequenceFile
#### saveAsObjectFile
#### foreach

## Control 算子
### persist
### cache
### unpersist
### checkpoint

## 全局变量
### Broadcast
### Accumulators
