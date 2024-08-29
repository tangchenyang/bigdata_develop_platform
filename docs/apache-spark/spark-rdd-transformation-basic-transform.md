# Transformation 算子 - 基础转换
## map
对RDD的每一条记录做转换操作
```
scala> val intRDD = sc.range(0, 5)
intRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[0] at range at <console>:23

scala> val transformedRDD = intRDD.map(_ * 2)
transformedRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[1] at map at <console>:23cala> val transformedRDD = intRDD

scala> transformedRDD.collect
res0: Array[Long] = Array(0, 2, 4, 6, 8)
```
## filter
对RDD的每一条记录做过滤操作
```
scala> val intRDD = sc.range(0, 5)
intRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[0] at range at <console>:23

scala> val filteredRDD = intRDD.filter(_ <= 2)
filteredRDD: org.apache.spark.rdd.RDD[Long] = MapPartitionsRDD[1] at filter at <console>:23

scala> filteredRDD.collect
res0: Array[Long] = Array(0, 1, 2)
```
## flatMap
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
## sample
对RDD进行采样，返回样本记录, fraction 不代表精确的比例，仅代表每条记录被命中的概率
```
scala> val rdd = sc.parallelize(1 to 100)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val sampleRDD = rdd.sample(withReplacement=true, fraction=0.1)
sampleRDD: org.apache.spark.rdd.RDD[Int] = PartitionwiseSampledRDD[1] at sample at <console>:23

scala> sampleRDD.collect
res0: Array[Int] = Array(15, 17, 21, 21, 36, 43, 54, 59, 63, 67, 83, 83, 95)
```
## sampleByKey
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
## pipe
对RDD进行操作系统级的管道操作
```
scala> val rdd = sc.parallelize(1 to 100)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.pipe("grep 0").collect
res0: Array[String] = Array(10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
```
## zipWithIndex
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

## zipWithUniqueId
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
## sortBy
对 RDD 进行排序，将以用户指定的 U => V 函数的返回值作为排序依据  
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val descSortedRDD = rdd.sortBy(x => x, ascending=false)
sortedRDD: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[1] at sortBy at <console>:23

scala> descSortedRDD.collect
res0: Array[Int] = Array(6, 5, 4, 3, 2, 1)
```
## sortByKey
对 K-V Pair 型 RDD 按 Key 进行排序  
***只能作用于 K-V Pair 型 RDD***
``` 
scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val kvRDD = rdd.keyBy(x => x)
sortedRDD: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[1] at sortBy at <console>:23

scala> val ascSortedRDD = kvRDD.sortByKey(ascending=true)
ascSortedRDD: org.apache.spark.rdd.RDD[(Int, Int)] = ShuffledRDD[2] at sortByKey at <console>:23

scala> ascSortedRDD.collect
res0: Array[(Int, Int)] = Array((1,1), (2,2), (3,3), (4,4), (5,5), (6,6))
```
## distinct
对 RDD 进行去重, 完全相同的记录将被移除  
``` 
scala> val rdd = sc.parallelize(List("A" -> 1, "A" -> 1, "A" -> 11, "B" -> 2))
rdd: org.apache.spark.rdd.RDD[(String, Int)] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val distinctedRDD = rdd.distinct
distinctedRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[1] at distinct at <console>:23

scala> distinctedRDD.collect
res0: Array[(String, Int)] = Array((A,1), (B,2), (A,11))
```

## keyBy
为RDD的每一条记录生成一个 Key, 返回(key, record) 的元祖，key 由用户指定的 record => key 函数生成
```
scala> val rdd = sc.parallelize(1 to 6, 2)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedDF = rdd.keyBy { x => if (x % 2 == 0) "even" else "odd" }
transformedDF: org.apache.spark.rdd.RDD[(Int, Int)] = MapPartitionsRDD[1] at keyBy at <console>:23

scala> transformedDF.collect
res0: Array[(String, Int)] = Array((odd,1), (even,2), (odd,3), (even,4), (odd,5), (even,6))
```
## mapValues
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
## flatMapValues
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
