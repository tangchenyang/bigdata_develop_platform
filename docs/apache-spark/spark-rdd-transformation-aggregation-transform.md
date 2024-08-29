# Transformation 算子 - 聚合操作
## groupBy
对 RDD 按 key 进行分组, 具有相同 key 的记录会被 group 到一起, key 值由用户指定的 record => key 函数决定
```
scala> val rdd = sc.parallelize(1 to 6, 2)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val groupedRDD = rdd.groupBy { x => if (x % 2 == 0) "even" else "odd" }
transformedDF: org.apache.spark.rdd.RDD[(Int, Int)] = MapPartitionsRDD[1] at keyBy at <console>:23

scala> groupedRDD.collect
res0: Array[(String, Iterable[Int])] = Array((even,CompactBuffer(2, 4, 6)), (odd,CompactBuffer(1, 3, 5)))
```
## groupByKey
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
## reduceByKey
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
## foldByKey
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

## aggregateByKey
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
## combineByKey
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
## countApproxDistinctByKey
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
