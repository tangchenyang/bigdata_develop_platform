# Transformation 算子 - 集合运算
## union
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
## intersection
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
## subtract
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
## join
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
## cogroup
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
## groupWith
[cogroup](#cogroup) 的别名，行为与 cogroup 完全一致
## leftOuterJoin
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
## rightOuterJoin
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
## fullOuterJoin
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
## subtractByKey
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
## cartesian
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
## randomSplit
将RDD切分成一组RDD, 切分成多少组由权重 weights 的数组大小决定, 权重不代表精确的比例，仅代表每条记录被命中的概率
```
scala> val rdd = sc.parallelize(1 to 10)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val splitedRDDs = rdd.randomSplit(Array(0.2, 0.2, 0.6))
splitedRDDs: Array[org.apache.spark.rdd.RDD[Int]] = Array(MapPartitionsRDD[1] at randomSplit at <console>:23, MapPartitionsRDD[98] at randomSplit at <console>:23, MapPartitionsRDD[99] at randomSplit at <console>:23)

scala> splitedRDDs.map(_.collect)
res0: Array[Array[Int]] = Array(Array(2, 3, 6), Array(5, 7, 9), Array(1, 4, 8, 10))
```
## zip
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
