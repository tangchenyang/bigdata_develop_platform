# 共享变量
## Accumulators
由于 Spark 计算时会将程序及变量序列化之后发送到各个 partition ，因此在各个 task 中执行计算时，只会操作变量的副本，并不会更新 Driver 端的原变量  
如下面的例子中，看似更新了 sum 的值，实际上 Driver 端的 sum 仍然为 0
``` 
scala> var sum = 0
sum: Int = 0

scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.foreach(x => sum = sum + x)

scala> sum
res1: Int = 0
```
大多数场景中可以用 Spark 丰富的算子完成类似的需求。  
但为了应对不同的业务场景，Spark 仍然可更新的共享变量: 累加器(Accumulators)

累加器是仅支持添加的变量，其引用会被分发到每个 partition 中，因此能够支持在多个 task 中并行计算
### longAccumulator
long 类型累加器，提供 `add` 方法用来在 Executor 中并行添加元素，并提供 `value`, `sum`, `count`, `avg` 方法来在 Driver 获取结果
以及提供 `merge` 方法来合并其他累加器中的值
``` 
scala> val longAccum = sc.longAccumulator("long accumulator")
longAccum: org.apache.spark.util.LongAccumulator = LongAccumulator(id: 0, name: Some(long accumulator), value: 0)

scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> rdd.foreach(longAccum.add(_))

scala> longAccum.value
res1: Long = 21

scala> longAccum.sum
res2: Long = 21

scala> longAccum.count
res3: Long = 6

scala> longAccum.avg
res4: Double = 3.5

scala> longAccum.merge(longAccum)

scala> longAccum.value
res5: Long = 42

scala> longAccum.sum
res6: Long = 42

scala> longAccum.count
res7: Long = 12

scala> longAccum.avg
res8: Double = 3.5
```
### doubleAccumulator
double 类型累加器， 与 [longAccumulator](#longAccumulator) 行为一致，只是类型不同  
### collectionAccumulator
集合类型累加器，提供 `add` 方法用来在 Executor 中并行添加元素，并提供 `value` 方法来在 Driver 获取结果
以及提供 `merge` 方法来合并其他累加器中的值
```
scala> val collectionAccum = sc.collectionAccumulator[Int]("collection accumulator")
collectionAccum: org.apache.spark.util.CollectionAccumulator[Int] = CollectionAccumulator(id: 0, name: Some(collection accumulator), value: [])

scala> val rdd = sc.parallelize(1 to 6)
rdd: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala>  rdd.foreach(collectionAccum.add(_))

scala> collectionAccum.value
res0: java.util.List[Int] = [1, 2, 5, 6, 3, 4]

scala> collectionAccum.merge(collectionAccum)

scala> collectionAccum.value
res1: java.util.List[Int] = [1, 2, 5, 6, 3, 4, 1, 2, 5, 6, 3, 4]
``````

## Broadcast Variables
由于 Spark 计算时会将程序及变量序列化之后发送到各个 partition，当变量较大或者 task 数量较多的情况，拷贝和传输变量会占用很多 Driver 端的带宽资源  
因此 Spark 提供了广播变量(Broadcast Variables)，来将变量的只读副本分发到每台节点上面，该节点上的所有 task 可以直接从此只读副本中读取变量的值，从而降低计算时发生的网络传输成本  
``` 
scala> val broadcastMapping = sc.broadcast(Map("A" -> 1, "B" -> 2, "C" -> 3 ))
broadcastVariable: org.apache.spark.broadcast.Broadcast[scala.collection.immutable.Map[String,Int]] = Broadcast(0)

scala> broadcastMapping.value
res0: scala.collection.immutable.Map[String,Int] = Map(A -> 1, B -> 2, C -> 3)

scala> val rdd = sc.parallelize(List("A", "B", "C", "D"))
rdd: org.apache.spark.rdd.RDD[String] = ParallelCollectionRDD[0] at parallelize at <console>:23

scala> val transformedRDD = rdd.map(x => (x, broadcastMapping.value.getOrElse(x, 0)))
transformedRDD: org.apache.spark.rdd.RDD[(String, Int)] = MapPartitionsRDD[1] at map at <console>:24

scala> transformedRDD.collect
res1: Array[(String, Int)] = Array((A,1), (B,2), (C,3), (D,0))
```
