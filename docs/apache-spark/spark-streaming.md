# Spark Streaming

## Spark Streaming 简介
_Spark Streaming 是 Spark 中的上一代流计算引擎，目前作为一个遗留系统，Spark 3.4.0 之后已经停止更新。如果想从零开始一个 Spark 流处理的应用，请使用 Spark Structured Streaming, todo add link_  

Spark Streaming 是基于 Spark RDD API 抽象出来的流处理计算框架，核心思路是将无界的流数据按时间窗口切分成有界的数据集合，再交给 Spark 引擎对每个有界的数据集进行批处理操作。    
因此，Spark Streaming 并不是严格意义上的基于数据流的实时计算引擎，而是基于微批的准实时计算引擎，微批之间的间隔最低为1秒左右。但即便如此，也足以应对除了对大多数秒级或分钟级近实时计算的场景。  

![image](https://github.com/tangchenyang/picx-images-hosting/raw/master/20240816/image.7sn4vpg33o.webp)

## 创建 DStream 
DStream 是 Spark Streaming 基于 RDD 高度抽象的数据流 API，数据流可以从多种数据源获取，如 Socket、消息队列 Kafka、文件系统 HDFS/S3 等  
Spark Streaming 的操作都是基于 StreamingContext 的，因此需要先创建一个 sparkStreamingContext(ssc) 实例  
```scala
import org.apache.spark._
import org.apache.spark.streaming._

val sparkConf = new SparkConf().setMaster("local[*]")
val ssc = new StreamingContext(sparkConf, Seconds(1))
```
### Socket 
#### socketTextStream
根据指定的 hostname 和 port 创建一个基于 TCP Socket 的文本数据流  
``` scala 
val socketTextDStream = ssc.socketTextStream("localhost", 9999)
```
#### socketStream
与 [socketTextStream](#socketTextStream) 类似，但可以支持自定义的 converter，来将字节流转换为对象  

```scala
// define WordCount converter
case class WordCount(word: String, count: Int) extends Serializable
import java.io._
import collection.JavaConverters._
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
```
### 消息队列
### 文件系统
### 自定义 Receiver 
#### receiverStream

- socketTextStream
- socketStream
- rawSocketStream
- fileStream
- textFileStream
- binaryRecordsStream
- queueStream
- 
## Transformation 算子
## Action 算子
## 控制算子 

