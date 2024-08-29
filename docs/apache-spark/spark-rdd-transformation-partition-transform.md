# Transformation 算子 - 分区转换
## mapPartitions
对 RDD 的每一个分区做转换操作，每个分区中的元素被封装成一个迭代器，因此这个转换函数应是 iterator => iterator 的映射
```
scala> val rdd = sc.parallelize((1 to 6).map(_.toString), 3)
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rdd.mapPartitions{ iter => val salt = "abcd_"; iter.map(x=>salt + x) }
transformedRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[1] at mapPartitions at <console>:24

scala> transformedRDD.collect
res0: Array[String] = Array(abcd_1, abcd_2, abcd_3, abcd_4, abcd_5, abcd_6)
```
## mapPartitionsWithIndex
对 RDD 的每一个分区做转换操作，每个分区中的元素被封装成一个迭代器, 并拥有当前 partition 的 Index，因此这个转换函数应是 (partitionIndex, iterator) => iterator 的映射
```
scala> val rdd = sc.parallelize((1 to 6).map(_.toString), 3)
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rdd.mapPartitionsWithIndex{(idx, iter) => iter.map(x=> s"p_${idx}__${x}")}
transformedRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[1] at mapPartitionsWithIndex at <console>:23

scala> transformedRDD.collect
res0: Array[String] = Array(p_0__1, p_0__2, p_1__3, p_1__4, p_2__5, p_2__6)
```
## glom 
将 RDD 的每个分区中的所有记录合并成一个 Array
```
scala> val rdd = sc.parallelize((1 to 6).map(_.toString), 3)
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rdd.glom
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[1] at parallelize at <console>:23

scala> transformedRDD.collect
res0: Array[Array[String]] = Array(Array(1, 2), Array(3, 4), Array(5, 6))
```
## zipPartitions
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
## coalesce
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
## repartition
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
## partitionBy
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
