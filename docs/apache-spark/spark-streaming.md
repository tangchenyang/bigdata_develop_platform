# Spark Streaming

## Spark Streaming 简介
_Spark Streaming 是 Spark 中的上一代流计算引擎，目前作为一个遗留系统，Spark 3.4.0 之后已经停止更新。如果想从零开始一个 Spark 流处理的应用，请使用 Spark Structured Streaming, todo add link_  

Spark Streaming 是基于 Spark RDD API 抽象出来的流处理计算框架，核心思路是将无界的流数据按时间窗口切分成有界的数据集合，再交给 Spark 引擎对每个有界的数据集进行批处理操作。    
因此，Spark Streaming 并不是严格意义上的基于数据流的实时计算引擎，而是基于微批的准实时计算引擎，微批之间的间隔最低为1秒左右。但即便如此，也足以应对除了对大多数秒级或分钟级近实时计算的场景。  

![image](https://github.com/tangchenyang/picx-images-hosting/raw/master/20240816/image.7sn4vpg33o.webp)

## 创建 DStream 
DStream (Discretized Stream) 是 Spark Streaming 基于 RDD 高度抽象的离散化数据流 API，数据流可以从多种数据源获取，如 Socket、消息队列 Kafka、文件系统 HDFS/S3 等  
Spark Streaming 的操作都是基于 StreamingContext 的，因此需要先创建一个 sparkStreamingContext(ssc) 实例  
```scala
import org.apache.spark._
import org.apache.spark.streaming._

val sparkConf = new SparkConf().setMaster("local[*]")
val ssc = new StreamingContext(sparkConf, Seconds(5))
ssc.checkpoint("checkpoint")
```
### Socket 
#### socketTextStream
根据指定的 hostname 和 port 创建一个基于 TCP Socket 的文本数据流   
Example: [sparkstream/SocketTextStreamExample](/spark-example/src/main/scala/org/exmaple/spark/sparkstreaming/SocketTextStreamExample.scala)
```scala 
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据  
``` 
$ nc -lk 9999
a
b
c
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据 
``` 
-------------------------------------------
Time: 1724326720000 ms
-------------------------------------------
a
b
c
```

#### socketStream
与 [socketTextStream](#socketTextStream) 类似，但可以支持自定义的 converter，来将字节流转换为类对象  
Example: [sparkstream/SocketStreamExample](/spark-example/src/main/scala/org/exmaple/spark/sparkstreaming/SocketTextStreamExample.scala)

```scala
// define class WordCount 
case class WordCount(word: String, count: Int) extends Serializable

// define custom converter
def convertBytesToWords(inputStream: InputStream): Iterator[WordCount] = {
  val dataInputStream = new BufferedReader(
    new InputStreamReader(inputStream, "UTF-8")
  )
  val linesIterator = dataInputStream.lines().iterator().asScala
  val wordsIterator = linesIterator.flatMap(_.split(" "))
  val wordCountIterator = wordsIterator.map(new WordCount(_, 1))
  wordCountIterator
}

// create socket stream
val socketWordCountDStream = ssc.socketStream[WordCount](
  "localhost", 9999, convertBytesToWords, StorageLevel.MEMORY_AND_DISK_SER_2
)
socketWordCountDStream.print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
a
b b
c c c
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据
``` 
-------------------------------------------
Time: 1724326945000 ms
-------------------------------------------
WordCount(a,1)
WordCount(b,1)
WordCount(b,1)
WordCount(c,1)
WordCount(c,1)
WordCount(c,1)
```

### 消息队列
Spark Streaming 支持与消息队列系统集成，如 Kafka 等  
#### Kafka
根据指定的 Kafka Topic 创建一个持续消费 Kafka Message 的 DStream  
Spark Streaming 与 Kafka 集成需要引入 `org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.1` 依赖  
Example: [sparkstream/KafkaStreamExample](/spark-example/src/main/scala/org/exmaple/spark/sparkstreaming/KafkaStreamExample.scala)
```scala
import org.apache.kafka.clients.consumer.ConsumerRecord
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.streaming.dstream.InputDStream
import org.apache.spark.streaming.kafka010.{ConsumerStrategies, KafkaUtils, LocationStrategies}

val subscribeTopics = Array("test-topic")
val kafkaParams = Map[String, Object](
  "bootstrap.servers" -> "localhost:9092",
  "key.deserializer" -> classOf[StringDeserializer],
  "value.deserializer" -> classOf[StringDeserializer],
  "group.id" -> "test_group",
  "auto.offset.reset" -> "earliest",
  "enable.auto.commit" -> "false"
)

val kafkaDStream: InputDStream[ConsumerRecord[String, String]] = KafkaUtils.createDirectStream[String, String](
  ssc,
  LocationStrategies.PreferConsistent,
  ConsumerStrategies.Subscribe[String, String](subscribeTopics, kafkaParams)
)

val kafkaMessageDStream = kafkaDStream.map(_.value)

kafkaMessageDStream.print()
```
启动程序后，使用 kafka-producer 命令往本地的 kafka 发送一些消息 
``` 
$ kafka-console-producer.sh --broker-list localhost:9092 --topic test-topic
>a
>bb
>ccc

```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据
``` 
-------------------------------------------
Time: 1724327280000 ms
-------------------------------------------
a 
bb
ccc
```

### 文件系统
#### textFileStream
根据指定的文件系统目录创建一个 DStream，用来监控目录中的新添加的文件，并将这些新文件的每一行读取为 DStream 中的每一条记录  
Example: [sparkstream/TextFileStreamExample](/spark-example/src/main/scala/org/exmaple/spark/sparkstreaming/TextFileStreamExample.scala)

```scala
val textFileStream = ssc.textFileStream("/tmp/spark/logs/")
textFileStream.print()
```
启动程序后，使用 Linux 命令往该目录下写入一些文件
``` 
$ mkdir -p /tmp/spark/logs/
$ echo "a" > /tmp/spark/logs/a.txt
$ echo "bbb" > /tmp/spark/logs/b.txt
$ echo "ccc" > /tmp/spark/logs/c.txt
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据
``` 
-------------------------------------------
Time: 1724327465000 ms
-------------------------------------------
ccc
bbb
a
```
### 自定义 Receiver 
#### receiverStream
todo 

## Transformation 算子
### 基本转换
#### map
对 DStream 中的每一条记录，根据给定的 U => V 函数做转换操作  
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream.map(_.toUpperCase).print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
AAA
BBB
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及转换后的数据  
``` 
-------------------------------------------
Time: 1724327765000 ms
-------------------------------------------
AAA
BBB

-------------------------------------------
Time: 1724327765000 ms
-------------------------------------------
aaa
bbb
```
#### flatMap
对 DStream 中的每一条记录，根据给定的 U => V 函数做转换操作，同时当 V 为集合时，将集合中的元素展开成多行  

```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream.flatMap(_.split(" ")).print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
a a
b b b
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及转换后的数据
``` 
-------------------------------------------
Time: 1724327990000 ms
-------------------------------------------
a a
b b b

-------------------------------------------
Time: 1724327990000 ms
-------------------------------------------
a
a
b
b
b
```
#### filter
对 DStream 中的每一条记录做过滤操作
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream.filter(_.length >= 2).print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
a
bb
ccc
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及转换后的数据
``` 
-------------------------------------------
Time: 1724328160000 ms
-------------------------------------------
a
bb
ccc

-------------------------------------------
Time: 1724328160000 ms
-------------------------------------------
bb
ccc
```

#### mapValues
对  K-V Pair 型 DStream 中的每一条记录的 values 进行转换  
***只能作用于 K-V Pair 型 DStream***  
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream.map((_, 1)).mapValues(_ * 2).print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
a
b
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及转换后的数据  
``` 
-------------------------------------------
Time: 1724328160000 ms
-------------------------------------------
a
b
-------------------------------------------
Time: 1724328160000 ms
-------------------------------------------
(a,2)
(b,2)
```

#### flatMapValues
对 K-V Pair 型 DStream 的每一条记录中的列做转换操作，同时结果将数组中的元素展开成多行  
***只能作用于 K-V Pair 型 DStream***  
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream
  .map(line => (line, line))
  .flatMapValues(_.split(" ").toList)
  .print()

```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
a1 a2
b1 b2
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及转换后的数据
``` 
-------------------------------------------
Time: 1724400550000 ms
-------------------------------------------
a1 a2
b1 b2
-------------------------------------------
Time: 1724400550000 ms
-------------------------------------------
(a1 a2,a1)
(a1 a2,a2)
(b1 b2,b1)
(b1 b2,b2)
```

### 分区转换
#### repartition
将 DStream 每个批次中的 RDD 的 partition 到目标数量，对数据进行随机重新分布，会产生 Shuffle
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.foreachRDD(rdd => println("number of partitions before repartition: " + rdd.partitions.length))
socketTextDStream.repartition(10).foreachRDD(rdd => println("number of partitions after repartition: " + rdd.partitions.length))
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
aa
bb
```
Spark Streaming 任务的控制台将打印出 repartition 前后的分区数
``` 
number of partitions before repartition: 2
number of partitions after repartition: 10
```
#### mapPartitions
对 DStream 每个批次中的 RDD 的每一个分区做转换操作，每个分区中的元素被封装成一个迭代器，因此这个转换函数应是 iterator => iterator 的映射
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream.mapPartitions(iter => iter.map(_.toUpperCase)).print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
aa
bb
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及转换后的数据

``` 
-------------------------------------------
Time: 1724329090000 ms
-------------------------------------------
aa
bb

-------------------------------------------
Time: 1724329090000 ms
-------------------------------------------
AA
BB
```

### 聚合操作
#### glom
将 DStream 每个批次中的 RDD 的每个分区中的所有记录合并成一个 Array  
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream.glom().map(_.mkString(", ")).print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
aa
bb
cc
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及 glom 后的数据

``` 
-------------------------------------------
Time: 1724329215000 ms
-------------------------------------------
aa
bb
cc

-------------------------------------------
Time: 1724329215000 ms
-------------------------------------------
aa, bb
cc
```
#### reduce
对 DStream 每个批次中的 RDD 做聚合操作  
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream.reduce(_ + _).print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
aa
bb
cc
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及 reduce 后的数据

``` 
-------------------------------------------
Time: 1724329430000 ms
-------------------------------------------
aa
bb
cc

-------------------------------------------
Time: 1724329430000 ms
-------------------------------------------
aabbcc
```
#### count
对 DStream 每个批次中的 RDD 求 count 
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream.count().print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
aa
bb
cc
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及 count 后的数据

``` 
-------------------------------------------
Time: 1724329505000 ms
-------------------------------------------
aa
bb
cc

-------------------------------------------
Time: 1724329505000 ms
-------------------------------------------
3
```
#### countByValue
对 DStream 每个批次中的 RDD 的每一条记录求 count   
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream.countByValue().print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
aa
aa
bb
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及汇总后的数据

``` 
-------------------------------------------
Time: 1724329590000 ms
-------------------------------------------
aa
aa
bb

-------------------------------------------
Time: 1724329590000 ms
-------------------------------------------
(aa,2)
(bb,1)

```
#### groupByKey
对 K-V Pair 型 DStream 每个批次中的 RDD 按 key 进行分组, 具有相同 key 的记录会被 group 到一起  
***只能作用于 K-V Pair 型 DStream***
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream
  .map(line => line.split(",")(0) -> line.split(",")(1))
  .groupByKey()
  .print()

```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
a,a1
a,a2
b,b1
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及汇总后的数据

``` 
-------------------------------------------
Time: 1724401770000 ms
-------------------------------------------
a,a1
a,a2
b,b1
-------------------------------------------
Time: 1724401770000 ms
-------------------------------------------
(a,ArrayBuffer(a1, a2))
(b,ArrayBuffer(b1))
```
#### reduceByKey
对 K-V Pair 型 DStream 每个批次中的 RDD 按 key 进行 reduce 操作, 具有相同 key 的记录将按照用户指定的 (left, right) => result 函数从左到右进行合并
***只能作用于 K-V Pair 型 DStream***
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream
  .map(line => line.split(",")(0) -> line.split(",")(1))
  .groupByKey()
  .print()

```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
a,a1
a,a2
b,b1
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及汇总后的数据

``` 
-------------------------------------------
Time: 1724401885000 ms
-------------------------------------------
a,a1
a,a2
b,b1
-------------------------------------------
Time: 1724401885000 ms
-------------------------------------------
(a,a1a2)
(b,b1)

```
#### combineByKey
对 DStream 每个批次中的 RDD 进行合并操作，与 [rdd-combineByKey](spark-rdd.md#combinebykey) 行为一致，操作分两个阶段，先对单个分区内的数据聚合，再对所有分区聚合结果进行聚合，从而得到最终的聚合结果  
它允许返回一个与 DStream 记录类型 V 不同的类型 U, 比如将元素(Int) group 成一个 List   
同样需要两个聚合函数，以及一个用来创建初始值的函数, 这个函数的入参将是每个分区的第一个元素  
- createCombiner: V => U, 用于创建每个分区的初始值  
- mergeValue: (U, V) => U, 作用在每个分区内数据的聚合函数  
- mergeCombiners: (U, U) => U, 作用在每个分区聚合结果上的聚合函数  
- partitioner, 用来对数据进行重分区的 partitioner, 一般无特殊要求，给 HashPartitioner 即可
***只能作用于 K-V Pair 型 DStream***
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream
  .map(line => line.split(",")(0) -> line.split(",")(1))
  .combineByKey[List[String]](
    createCombiner = (s: String) => List[String](s),
    mergeValue = (l: List[String], s: String) => l :+ s,
    mergeCombiner = (l1: List[String], l2: List[String]) => l1 ++ l2,
    partitioner = new HashPartitioner(ssc.sparkContext.defaultMinPartitions))
  .print()

```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
a,a1
a,a2
b,b1
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及汇总后的数据

``` 
-------------------------------------------
Time: 1724402650000 ms
-------------------------------------------
a,a1
a,a2
b,b1
-------------------------------------------
Time: 1724402650000 ms
-------------------------------------------
(b,List(b1))
(a,List(a1, a2))
```

### 集合操作
#### union
将当前 DStream 与另一个 DStream 的数据统一起来，返回一个新的 DStream，两个 DStream 的滑动窗口间隔必须相同  
***作用于滑动窗口时，两个滑动窗口必须有相同的滑动时间***  
```scala
val socketTextDStream9999 = ssc.socketTextStream("localhost", 9999)
val socketTextDStream9998 = ssc.socketTextStream("localhost", 9998)

socketTextDStream9999.print()
socketTextDStream9998.print()
socketTextDStream9999.union(socketTextDStream9998).print()

```
启动程序后，使用 netcat 命令往本机的 9999 和 9998 端口发送一些数据
``` 
$ nc -lk 9999
aa
bb

$ nc -lk 9998
11
22
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及 union 后的数据
``` 
-------------------------------------------
Time: 1724328350000 ms
-------------------------------------------
aa
bb

-------------------------------------------
Time: 1724328350000 ms
-------------------------------------------
11
22

-------------------------------------------
Time: 1724328350000 ms
-------------------------------------------
aa
bb
11
22
```
#### cogroup
将两个 DStream 每个批次中的 RDD 按 Key 关联在一起，返回关联后的 DStream，相同 Key 的 value 会被 group 到一个集合中  
***只能作用于 K-V Pair 型 DStream***  
***作用于滑动窗口时，两个滑动窗口必须有相同的滑动时间***  
```scala
val socketTextDStream9999 = ssc.socketTextStream("localhost", 9999)
val socketTextDStream9998 = ssc.socketTextStream("localhost", 9998)

val kvDStream9999 = socketTextDStream9999.map(line => line.split(",")(0) -> line.split(",")(1))
val kvDStream9998 = socketTextDStream9998.map(line => line.split(",")(0) -> line.split(",")(1))

socketTextDStream9999.print()
socketTextDStream9998.print()

kvDStream9999.cogroup(kvDStream9998).print()

```
启动程序后，使用 netcat 命令往本机的 9999 和 9998 端口发送一些数据
``` 
$ nc -lk 9999
a,a1
a,a2
b,b1

$ nc -lk 9998
a,A1
a,A1
b,B1

```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及 cogroup 后的数据
``` 
-------------------------------------------
Time: 1724403410000 ms
-------------------------------------------
a,a1
a,a2
b,b1
-------------------------------------------
Time: 1724403410000 ms
-------------------------------------------
a,A1
a,A1
b,B1
-------------------------------------------
Time: 1724403410000 ms
-------------------------------------------
(a,(CompactBuffer(a1, a2),CompactBuffer(A1, A1)))
(b,(CompactBuffer(b1),CompactBuffer(B1)))
```

#### join
将当前 DStream 每个批次中的 RDD 与另外的 DStream 对应批次中的 RDD 进行关联,，返回关联后的 DStream，对于重复 value，会单独出现在不同记录中  
***只能作用于 K-V Pair 型 DStream***
```scala
val socketTextDStream9999 = ssc.socketTextStream("localhost", 9999)
val socketTextDStream9998 = ssc.socketTextStream("localhost", 9998)

val kvDStream9999 = socketTextDStream9999.map(line => line.split(",")(0) -> line.split(",")(1))
val kvDStream9998 = socketTextDStream9998.map(line => line.split(",")(0) -> line.split(",")(1))

socketTextDStream9999.print()
socketTextDStream9998.print()

kvDStream9999.join(kvDStream9998).print()

```
启动程序后，使用 netcat 命令往本机的 9999 和 9998 端口发送一些数据
``` 
$ nc -lk 9999
1,a
2,b

$ nc -lk 9998
1,A
2,B
2,Bb
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及 join 后的数据
``` 
-------------------------------------------
Time: 1724403920000 ms
-------------------------------------------
1,a
2,b
-------------------------------------------
Time: 1724403920000 ms
-------------------------------------------
1,A
2,B
2,Bb
-------------------------------------------
Time: 1724403920000 ms
-------------------------------------------
(2,(b,B))
(2,(b,Bb))
(1,(a,A))
```
#### leftOuterJoin
将当前 DStream 每个批次中的 RDD 与另外的 DStream 对应批次中的 RDD 进行左关联, 结果集中仅包含左 DStream 中的全部记录，右 DStream 中匹配不到的数据置为空  
即对于每一条记录 (key, value_left), 能匹配到时返回 (key, (value_left, value_right)), 匹配不到时返回(key, (value_left, None))  
***只能作用于 K-V Pair 型 DStream***  
***作用于滑动窗口时，两个滑动窗口必须有相同的滑动时间***
```scala
val socketTextDStream9999 = ssc.socketTextStream("localhost", 9999)
val socketTextDStream9998 = ssc.socketTextStream("localhost", 9998)

val kvDStream9999 = socketTextDStream9999.map(line => line.split(",")(0) -> line.split(",")(1))
val kvDStream9998 = socketTextDStream9998.map(line => line.split(",")(0) -> line.split(",")(1))

socketTextDStream9999.print()
socketTextDStream9998.print()

kvDStream9999.leftOuterJoin(kvDStream9998).print()

```
启动程序后，使用 netcat 命令往本机的 9999 和 9998 端口发送一些数据
``` 
$ nc -lk 9999
1,a
2,b
3,c

$ nc -lk 9998
1,A
2,B
2,Bb
4,D

```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及 leftOuterJoin 后的数据
``` 
-------------------------------------------
Time: 1724404360000 ms
-------------------------------------------
1,a
2,b
3,c
-------------------------------------------
Time: 1724404360000 ms
-------------------------------------------
1,A
2,B
2,Bb
4,D
-------------------------------------------
Time: 1724404360000 ms
-------------------------------------------
(2,(b,Some(B)))
(2,(b,Some(Bb)))
(3,(c,None))
(1,(a,Some(A)))
```
#### rightOuterJoin
将当前 DStream 每个批次中的 RDD 与另外的 DStream 对应批次中的 RDD 进行右关联, 结果集中仅包含右 DStream 中的全部记录，左 DStream 中匹配不到的数据置为空  
即对于每一条记录 (key, value_left), 能匹配到时返回 (key, (value_left, value_right)), 匹配不到时返回(key, (None, value_right))  
***只能作用于 K-V Pair 型 DStream***  
***作用于滑动窗口时，两个滑动窗口必须有相同的滑动时间***
```scala
val socketTextDStream9999 = ssc.socketTextStream("localhost", 9999)
val socketTextDStream9998 = ssc.socketTextStream("localhost", 9998)

val kvDStream9999 = socketTextDStream9999.map(line => line.split(",")(0) -> line.split(",")(1))
val kvDStream9998 = socketTextDStream9998.map(line => line.split(",")(0) -> line.split(",")(1))

socketTextDStream9999.print()
socketTextDStream9998.print()

kvDStream9999.rightOuterJoin(kvDStream9998).print()

```
启动程序后，使用 netcat 命令往本机的 9999 和 9998 端口发送一些数据
``` 
$ nc -lk 9999
1,a
2,b
3,c

$ nc -lk 9998
1,A
2,B
2,Bb
4,D

```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及 rightOuterJoin 后的数据
``` 
-------------------------------------------
Time: 1724404360000 ms
-------------------------------------------
1,a
2,b
3,c
-------------------------------------------
Time: 1724404360000 ms
-------------------------------------------
1,A
2,B
2,Bb
4,D
-------------------------------------------
Time: 1724404360000 ms
-------------------------------------------
(2,(Some(b),B))
(2,(Some(b),Bb))
(4,(None,D))
(1,(Some(a),A))
```

#### fullOuterJoin
将当前 DStream 每个批次中的 RDD 与另外的 DStream 对应批次中的 RDD 进行全关联, 结果集中将包含左右 RDD 中的全部记录，匹配不到的数据置为空  
即对于每一条记录 (key, value_left), 能匹配到时返回 (key, (value_left, value_right)), 匹配不到时返回(key, (value_left, value_right)) 或 (key, (None, value_right))  
***只能作用于 K-V Pair 型 DStream***  
***作用于滑动窗口时，两个滑动窗口必须有相同的滑动时间***
```scala
val socketTextDStream9999 = ssc.socketTextStream("localhost", 9999)
val socketTextDStream9998 = ssc.socketTextStream("localhost", 9998)

val kvDStream9999 = socketTextDStream9999.map(line => line.split(",")(0) -> line.split(",")(1))
val kvDStream9998 = socketTextDStream9998.map(line => line.split(",")(0) -> line.split(",")(1))

socketTextDStream9999.print()
socketTextDStream9998.print()

kvDStream9999.fullOuterJoin(kvDStream9998).print()

```
启动程序后，使用 netcat 命令往本机的 9999 和 9998 端口发送一些数据
``` 
$ nc -lk 9999
1,a
2,b
3,c

$ nc -lk 9998
1,A
2,B
2,Bb
4,D

```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及 fullOuterJoin 后的数据
``` 
-------------------------------------------
Time: 1724404360000 ms
-------------------------------------------
1,a
2,b
3,c
-------------------------------------------
Time: 1724404360000 ms
-------------------------------------------
1,A
2,B
2,Bb
4,D
-------------------------------------------
Time: 1724404360000 ms
-------------------------------------------
(2,(Some(b),Some(B)))
(2,(Some(b),Some(Bb)))
(3,(Some(c),None))
(4,(None,Some(D)))
(1,(Some(a),Some(A)))
```

### 窗口函数
#### window
生成一个新的 DStream，这个 DStream 以固定的时间宽度(windowDuration)以及滑动时间(slideDuration)的滑动窗口将数据聚集起来  
滑动窗口中将包含该窗口时间宽度内的所有记录，其时间宽度和滑动时间必须是当前 DStream 的计算间隔的整数倍  
- windowDuration: 滑动窗口的时间宽度。假设其值计算间隔的两倍，那么每当滑动窗口触发时，窗口内的数据将包含当前微批以及上一个微批中的所有记录  
- slideDuration：滑动窗口的滑动时间。即生成新的滑动窗口的时间间隔   

```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
// 滑动窗口时间设置为 10 s (当前计算间隔的两倍)
socketTextDStream
  .window(windowDuration = Durations.seconds(10), slideDuration = Durations.seconds(5))
  .print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据，其中 `aa` 和 `bb` 发完等待5秒再发 `cc` 确保他们被两个批次处理
``` 
$ nc -lk 9999
aa
bb
cc

```
Spark Streaming 任务的控制台将打印出从 socket 接收到的当前微批的数据，以及滑动窗口中数据。  
由于滑动设置为计算间隔的两倍，因此滑动窗口中将同时包含当前的微批和上一个微批中的数据  

``` 
-------------------------------------------
Time: 1724380055000 ms  // 第一个微批中的数据
-------------------------------------------
aa
bb

-------------------------------------------
Time: 1724380055000 ms  // 第一个滑动窗口中的数据。 由于上一个微批中无数据，因此当前滑动窗口中的数据等于当前微批中的数据 `aa` `bb`
-------------------------------------------
aa
bb

-------------------------------------------
Time: 1724380060000 ms  // 第二个微批中的数据
-------------------------------------------
cc

-------------------------------------------
Time: 1724380060000 ms  // 第二个滑动窗口中的数据。 当前滑动窗口中中包含当前微批中的数据 `cc` 与上一个微批中的数据 `aa` `bb`
-------------------------------------------
aa
bb
cc

```
#### reduceByWindow
对 DStream 每个滑动窗口中的 RDD 做聚合操作，相当于先对 DStream 开窗 [window](#window)，再对每个滑动窗口进行 [reduce](#reduce) 操作  
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream
  .reduceByWindow(_ + _, windowDuration = Durations.seconds(10), slideDuration = Durations.seconds(5))
  .print()
//socketTextDStream
//  .window(windowDuration = Durations.seconds(10), slideDuration = Durations.seconds(5))
//  .reduce(_ + _)
//  .print()

```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据，其中 `aa` 和 `bb` 发完等待5秒再发 `cc` 确保他们被两个批次处理
``` 
$ nc -lk 9999
aa
bb
cc

```
Spark Streaming 任务的控制台将打印出从 socket 接收到的当前微批的数据，以及滑动窗口中的聚合数据   
``` 
-------------------------------------------
Time: 1724395980000 ms  // 第一个微批中的数据
-------------------------------------------
aa
bb

-------------------------------------------
Time: 1724395980000 ms  // 第一个滑动窗口中的数据
-------------------------------------------
aabb

-------------------------------------------
Time: 1724395985000 ms  // 第二个微批中的数据
-------------------------------------------
cc

-------------------------------------------
Time: 1724395985000 ms  // 第二个滑动窗口中的数据
-------------------------------------------
aabbcc

```
#### countByWindow
对 DStream 每个窗口中的 RDD 求 count，相当于先对 DStream 开窗 [window](#window)，再对每个滑动窗口进行 [count](#count) 操作
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream
  .countByWindow(windowDuration = Durations.seconds(10), slideDuration = Durations.seconds(5))
  .print()
//socketTextDStream
//  .window(windowDuration = Durations.seconds(10), slideDuration = Durations.seconds(5))
//  .count()
//  .print()

```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据，其中 `aa` 和 `bb` 发完等待5秒再发 `cc` 确保他们被两个批次处理
``` 
$ nc -lk 9999
aa
bb
cc

```
Spark Streaming 任务的控制台将打印出从 socket 接收到的当前微批的数据，以及滑动窗口中的聚合数据
``` 
-------------------------------------------
Time: 1724395980000 ms  // 第一个微批中的数据
-------------------------------------------
aa
bb

-------------------------------------------
Time: 1724395980000 ms  // 第一个滑动窗口中的数据
-------------------------------------------
2

-------------------------------------------
Time: 1724395985000 ms  // 第二个微批中的数据
-------------------------------------------
cc

-------------------------------------------
Time: 1724395985000 ms  // 第二个滑动窗口中的数据
-------------------------------------------
3

```
#### groupByKeyAndWindow
对 DStream 每个滑动窗口中的 RDD 按 Key 做聚合操作，相当于先对 DStream 开窗 [window](#window)，再对每个滑动窗口进行 [groupByKey](#groupByKey) 操作  
***只能作用于 K-V Pair 型 DStream***
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream
  .map(line => line.split(",")(0) -> line.split(",")(1))
  .groupByKeyAndWindow(windowDuration = Durations.seconds(10), slideDuration = Durations.seconds(5))
  .print()
//socketTextDStream
//  .map(line => line.split(",")(0) -> line.split(",")(1))
//  .window(windowDuration = Durations.seconds(10), slideDuration = Durations.seconds(5))
//  .reduceByKey(_ + _)
//  .print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据，其中 `a,a1` 和 `a,a2` 发完等待5秒再发 `b,b1` 确保他们被两个批次处理
``` 
$ nc -lk 9999
a,a1
a,a2
b,b1
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的当前微批的数据，以及滑动窗口中的聚合数据
``` 
-------------------------------------------
Time: 1724405275000 ms
-------------------------------------------
a,a1
a,a2
-------------------------------------------
Time: 1724405275000 ms
-------------------------------------------
(a,ArrayBuffer(a1, a2))
-------------------------------------------
Time: 1724405280000 ms
-------------------------------------------
b,b1
-------------------------------------------
Time: 1724405280000 ms
-------------------------------------------
(a,ArrayBuffer(a1, a2))
(b,ArrayBuffer(b1))
```
#### reduceByKeyAndWindow
对 DStream 每个滑动窗口中的 RDD 按 Key 做聚合操作，相当于先对 DStream 开窗 [window](#window)，再对每个滑动窗口进行 [reduceByKey](#reduceByKey) 操作
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
socketTextDStream
  .map(line => line.split(",")(0) -> line.split(",")(1))
  .reduceByKeyAndWindow(_ + _, windowDuration = Durations.seconds(10), slideDuration = Durations.seconds(5))
  .print()
//socketTextDStream
//  .map(line => line.split(",")(0) -> line.split(",")(1))
//  .window(windowDuration = Durations.seconds(10), slideDuration = Durations.seconds(5))
//  .reduceByKey(_ + _)
//  .print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据，其中 `a,a1` 和 `a,a2` 发完等待5秒再发 `b,b1` 确保他们被两个批次处理
``` 
$ nc -lk 9999
a,a1
a,a2
b,b1
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的当前微批的数据，以及滑动窗口中的聚合数据
``` 
-------------------------------------------
Time: 1724405005000 ms
-------------------------------------------
a,a1
a,a2
-------------------------------------------
Time: 1724405005000 ms
-------------------------------------------
(a,a1a2)
-------------------------------------------
Time: 1724405010000 ms
-------------------------------------------
b,b1
-------------------------------------------
Time: 1724405010000 ms
-------------------------------------------
(a,a1a2)
(b,b1)
```

#### slice
### 状态算子

#### updateStateByKey
维护 DStream 的 Key 的全局状态，根据指定的 (values: scala.collection.Seq[U], state: Option[V]) => Option(V) 函数 进行状态更新  
每个批次中相同 Key 的 value 将被 group 成 values，当前 Key 的状态为 state  
***只能作用于 K-V Pair 型 DStream***
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
val tatalCountByKey: (Seq[Int], Option[Int]) => Option[Int] = (values: Seq[Int], state: Option[Int]) => {
  Some(values.sum + state.getOrElse(0))
}
socketTextDStream.print()
socketTextDStream
  .flatMap(_.split(" ")).map((_, 1))
  .updateStateByKey(tatalCountByKey)
  .print()


```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据，其中 `a` 和 `b` 发完等待5秒再发 `a a` 和 `b b` 确保他们被两个批次处理

``` 
$ nc -lk 9999
a
b 
a a
b b 
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及更新后的状态数据

``` 
-------------------------------------------
Time: 1724409375000 ms
-------------------------------------------
a
b 
-------------------------------------------
Time: 1724409375000 ms
-------------------------------------------
(a,1)
(b,1)
-------------------------------------------
Time: 1724409380000 ms
-------------------------------------------
a a
b b 
-------------------------------------------
Time: 1724409380000 ms
-------------------------------------------
(a,3)
(b,3)
```
#### mapWithState
维护 DStream 的 Key 的全局状态，根据指定的  (Time, String, Option[U], State[U]) => Some[V] 函数 进行状态更新  
每个批次中每个 Key 的每条记录，以及每个 Key 的当前状态都将作为参数传入函数进行计算，可根据 State 的 `exists`, `get`, `update` 等方法来维护状态  
***只能作用于 K-V Pair 型 DStream***
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)

val totalCountByKey: (Time, String, Option[Int], State[Int]) => Some[(String, Int)] = (time: Time, key: String, value: Option[Int], state: State[Int]) => {
  if (!state.exists())
    state.update(0)
  else {
    state.update(state.get() + value.getOrElse(0))
  }
  Some({key -> state.get()})
}

socketTextDStream.print()
socketTextDStream
  .flatMap(_.split(" ")).map((_, 1))
  .mapWithState(StateSpec.function(totalCountByKey))
  .print()

```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据，其中 `a` 和 `b` 发完等待5秒再发 `a a` 和 `b b` 确保他们被两个批次处理

``` 
$ nc -lk 9999
a
b 
a a
b b 
```
Spark Streaming 任务的控制台将打印出从 socket 接收到的数据，以及更新后的状态数据

``` 
-------------------------------------------
Time: 1724410525000 ms
-------------------------------------------
a
b 

-------------------------------------------
Time: 1724410525000 ms
-------------------------------------------
(a,1)
(b,1)
-------------------------------------------
Time: 1724410530000 ms
-------------------------------------------
a a
b b 
-------------------------------------------
Time: 1724410530000 ms
-------------------------------------------
(a,2)
(a,3)
(b,2)
(b,3)

```

## Action 算子
### 转换为 Java 集合
#### foreachRDD
对 DStream 每个批次中的 RDD 做遍历操作，可以将 RDD 输出到控制台或写入外部系统等操作，返回 Unit 类型即无返回值  
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.foreachRDD(rdd => rdd.foreach(println(_)))
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
```
$ nc -lk 9999
aa
bb
cc

``` 
Spark Streaming 任务的控制台将打印出每个批次中的 RDD 的每一条记录
``` 
-------------------------------------------
Time: 1724415010000 ms
-------------------------------------------
(a,a1a2)
(b,b1)

```
#### print
将 DStream 每个批次中的 RDD 的前 10 条记录输出到控制台  
```scala
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
socketTextDStream.print()
```
启动程序后，使用 netcat 命令往本机的 9999 端口发送一些数据
```
$ nc -lk 9999
aa
bb
cc

``` 
Spark Streaming 任务的控制台将打印出每个批次中的 RDD 的每一条记录
``` 
-------------------------------------------
Time: 1724415010000 ms
-------------------------------------------
aa
bb
cc
```

### 输出到外部系统
#### saveAsTextFiles
将 DStream 每个批次中的 RDD 以 TEXT 文件格式写入 Hadoop 支持的外部文件系统
#### saveAsObjectFiles
将 DStream 每个批次中的 RDD 序列化之后，以 Hadoop SequenceFile 文件格式写入 Hadoop 支持的外部文件系统


## 控制算子 
### persist
将 DStream 每个批次中的 RDD 缓存到内存或者磁盘中，提升作业性能
### cache
等同于缓存级别为 `MEMORY_ONLY_SER` 的 [persist](#persist)
### checkpoint 
将当前的 DStream 按设置的间隔保存在设置的 checkpointDir 中，当程序重启时，将从最新 checkpoint 处继续运行 


