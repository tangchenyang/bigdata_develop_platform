# Spark Structured Streaming 
## 简介
Spark Structured Streaming 是基于 Spark SQL 构建的 Spark 第二代流处理引擎，它向提供了与批处理语义一致的 DataFrame API，因此可以在代码层面将批处理和流处理进行统一。 它的核心思想是，将数据流转换为无界的表，数据流中的每一条新纪录，都表示为无界表中的一条追加的行。  
Spark Structured Streaming 在默认情况下仍然使用微批(离散流)处理，来实现最低 100 毫秒的计算间隔，并通过 checkpoint 和预写日志 WAL (Write-Ahead Logs) 来实现端到端的精确一次处理（exactly-once）语义；
在 Spark 2.3 以引入了低延迟（连续流）处理模式，来满足最低 1 毫秒的端到端延迟，并实现端到端的至少一次处理(at-least once) 语义。  

## 创建流式 DataFrame  
Spark Structured Streaming 的操作是基于 Spark SQL 的，因此构建一个统一的 SparkSession ，通过 SparkSession 的 readStream 系列操作，即可将数据源读取为流式 DataFrame（）
```scala
import org.apache.spark.sql._

val spark = SparkSession.builder.appName("Structured Streaming Example")
  .master("local[*]")
  .getOrCreate()
```

### 读取 Socket  
根据指定的 hostname 和 port 将 Socket 中的文件数据读取为 DataFrame  
```scala  
// create socket streaming DataFrame
val socketStreamDataFrame: DataFrame = spark.readStream
  .format("socket")
  .option("host", "localhost")
  .option("port", 9999)
  .load()

println(f"isStreaming = ${socketStreamDataFrame.isStreaming}")

// print in console
socketStreamDataFrame.writeStream
  .format("console")
  .trigger(Trigger.ProcessingTime("5 seconds"))
  .start()
  .awaitTermination()
```
运行 netcat 保持 9999 端口打开，启动程序后，使用 netcat 往本机的 9999 端口发送一些数据
``` 
$ nc -lk 9999
a
b
c
```
Structured Streaming 任务的控制台将打印出当前计算批次以及从 socket 接收到的数据  
``` 
isStreaming = true

-------------------------------------------
Batch: 1
-------------------------------------------
+-----+
|value|
+-----+
|    a|
|    b|
|    c|
+-----+
```
### 用于测试的 Rate Source 
Structured Streaming 提供了两个 `Rate Source` 用于按照指定的的速率生成测试场景下的输入数据  
- `Rate Source`: format `rate`，按 `rowsPerSecond` 的速率，每秒生成指定数量的记录   
- `Rate Per Micro-Batch Source `: format `rate-micro-batch`，按 `rowsPerBatch` 的速率，每个批次生成指定数量的记录  
```scala 
// create rate streaming DataFrame
val rateStreamingDataFrame: DataFrame = spark.readStream
  .format("rate")
  .option("rowsPerSecond", "1")
  .load()

println(f"isStreaming = ${rateStreamingDataFrame.isStreaming}")

// print in console
rateStreamingDataFrame.writeStream
  .format("console")
  .trigger(Trigger.ProcessingTime("5 seconds"))
  .start()
  .awaitTermination()
```
程序启动后，控制台将打印出生成的数据
``` 
isStreaming = true

-------------------------------------------
Batch: 1
-------------------------------------------
+--------------------+-----+
|           timestamp|value|
+--------------------+-----+
|2024-08-26 10:10:...|    0|
|2024-08-26 10:10:...|   10|
|2024-08-26 10:10:...|   20|
+--------------------+-----+
```
### 读取外部文件系统
从外部文件系统（如 HDFS，S3等）将数据读取为 DataFrame  
```scala
// create text file streaming DataFrame
val textFilesStreamDataFrame: DataFrame = spark.readStream
  .option("header", "false")
  .text("file:///tmp/spark/input_txt_files/")

println(f"isStreaming = ${textFilesStreamDataFrame.isStreaming}")

// print in console
textFilesStreamDataFrame.writeStream
  .format("console")
  .trigger(Trigger.ProcessingTime("5 seconds"))
  .start()
  .awaitTermination()

```
Spark 在指定目录不存在时会抛出异常，因此先创建一个本地文件目录 `/tmp/spark/input_text_files/` 
```shell
mkdir -p /tmp/spark/input_text_files/
```
启动程序后，使用 Linux 命令往该目录下写入一些文件
```shell 
mkdir -p /tmp/spark/input_text_files/
echo "aaa" > /tmp/spark/input_text_files/a.txt
echo "bbb" > /tmp/spark/input_text_files/b.txt
echo "ccc" > /tmp/spark/input_text_files/c.txt

```
Streaming 任务的控制台将打印出从该路径识别到的文件中的数据
``` 
-------------------------------------------
Batch: 1
-------------------------------------------
+-----+
|value|
+-----+
|  aaa|
|  bbb|
|  ccc|
+-----+
```

### 读取流式表
从流式表中将数据读取为流式 DataFrame   
本例子中先通过 [Rate Source](#用于测试的-rate-source-) 创建数据流并将其创建为表，再从此流式表中读取数据，打印到控制台中   
```scala
// create rate streaming DataFrame
val rateStreamingDataFrame: DataFrame = spark.readStream
  .format("rate")
  .option("rowsPerSecond", "3")
  .load()
// write the rate streaming DataFrame to table
rateStreamingDataFrame.writeStream
  .option("checkpointLocation", "checkpoints/test")
  .outputMode("append")
  .toTable("temp_streaming_table")

// create streaming DataFrame from table
val streamingDataFrame: DataFrame = spark.readStream
  .table("temp_streaming_table")

// print in console
streamingDataFrame.writeStream
  .format("console")
  .trigger(Trigger.ProcessingTime("2 seconds"))
  .start()
  .awaitTermination()
```
程序运行后，控制台将打印出从表中读取到的数据   
``` 
-------------------------------------------
Batch: 1
-------------------------------------------
+--------------------+-----+
|           timestamp|value|
+--------------------+-----+
|2024-08-27 10:48:...|    9|
|2024-08-27 10:48:...|    3|
|2024-08-27 10:48:...|    2|
+--------------------+-----+
``` 

### 读取消息系统
从消息系统（如 Kafka）中将数据读取为流式 DataFrame  
#### Kafka 
根据指定的 Kafka Topic 创建一个持续消费 Kafka Message 的流式 DataFrame  
Spark Structured Streaming 与 Kafka 集成需要引入 `org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1` 依赖  
Example: [sparkstream/KafkaStreamExample](/spark-example/src/main/scala/org/exmaple/spark/structuredstreaming/)  

```scala
// create kafka streaming DataFrame
val kafkaStreamingDataFrame: DataFrame = spark.readStream
  .format("kafka")
  .option("kafka.bootstrap.servers", "localhost:9092")
  .option("subscribe", "test-topic")
  .load()

println(f"isStreaming = ${kafkaStreamingDataFrame.isStreaming}")

// print in console
kafkaStreamingDataFrame.withColumn("value", kafkaStreamingDataFrame("value").cast("string"))
  .writeStream
  .format("console")
  .trigger(Trigger.ProcessingTime("5 seconds"))
  .start()
  .awaitTermination()
```
启动程序后，使用 kafka-producer 命令往本地的 kafka 发送一些消息
``` 
$ kafka-console-producer.sh --broker-list localhost:9092 --topic test-topic
>a
>bb
>ccc
```
Streaming 任务的控制台将打印出从 Kafka Topic 接收到的数据  
``` 
isStreaming = true

-------------------------------------------
Batch: 1
-------------------------------------------
+----+-----+----------+---------+------+--------------------+-------------+
| key|value|     topic|partition|offset|           timestamp|timestampType|
+----+-----+----------+---------+------+--------------------+-------------+
|NULL|    a|test-topic|        0|    36|2024-08-27 12:12:...|            0|
|NULL|   bb|test-topic|        0|    37|2024-08-27 12:12:...|            0|
|NULL|  ccc|test-topic|        0|    38|2024-08-27 12:12:...|            0|
+----+-----+----------+---------+------+--------------------+-------------+
```
## Transformation 算子
### 基本转换
由于 Structured Streaming 使用与批处理语义一致的 DataFrame API，因此可以使用一切基于 DataFrame 的基本操作(如 select, where 等)，
详细内容请参考 [spark-dataframe](spark-dataframe.md#transformation-算子)  
### 窗口操作
Structured Streaming 有三种窗口类型：`翻滚窗口`、`滑动窗口` 和 `会话窗口`.  
![image](https://github.com/tangchenyang/picx-images-hosting/raw/master/20240827/image.8vmumr97ds.webp)  
#### 翻滚窗口
翻滚窗口(Tumbling Window) 是一系列不重叠但连续的、具有固定时间宽度的数据窗口。为了帮助理解，可以想象一下有一个正方形的卡片重复着翻滚动作，每次翻滚所产生的阴影面积即为一个一个的翻滚窗口  
下面的例子将以10s生成翻滚窗口，统计每个窗口中的记录数，由于使用 rate source 并按每秒3条记录发送数据，因此每个翻滚窗口中将最多包含30条记录  
另外由于 [outputMode](#输出模式) 设置为 `complete`，因此每个批次将显示所有窗口的结果  

```scala
// get job start time
val startTime = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").format(LocalDateTime.now)
println(f"Job start at ${startTime}")

// create rate streaming DataFrame
val rateStreamingDataFrame: DataFrame = spark.readStream
  .format("rate")
  .option("rowsPerSecond", "3")
  .load()

rateStreamingDataFrame
  .groupBy(window(col("timestamp"), w"10 seconds")).count()
  .writeStream
  .outputMode("complete")
  .format("console").option("truncate", "false")
  .trigger(Trigger.ProcessingTime("5 seconds"))
  .start()
  .awaitTermination()
```
程序启动后，控制台将打印出每个批次每个窗口中的数据  
``` 
Job start at 2024-08-27 19:09:29 
-------------------------------------------
Batch: 0
-------------------------------------------
+------+-----+------------+
|window|count|current_time|
+------+-----+------------+
+------+-----+------------+

-------------------------------------------
Batch: 1
-------------------------------------------
+------------------------------------------+-----+-----------------------+
|window                                    |count|current_time           |
+------------------------------------------+-----+-----------------------+
|{2024-08-27 19:09:30, 2024-08-27 19:09:40}|21   |2024-08-27 19:09:53.432|
|{2024-08-27 19:09:40, 2024-08-27 19:09:50}|30   |2024-08-27 19:09:53.432|
|{2024-08-27 19:09:50, 2024-08-27 19:10:00}|9    |2024-08-27 19:09:53.432|
+------------------------------------------+-----+-----------------------+

-------------------------------------------
Batch: 2
-------------------------------------------
+------------------------------------------+-----+-----------------------+
|window                                    |count|current_time           |
+------------------------------------------+-----+-----------------------+
|{2024-08-27 19:09:30, 2024-08-27 19:09:40}|21   |2024-08-27 19:10:04.201|
|{2024-08-27 19:09:40, 2024-08-27 19:09:50}|30   |2024-08-27 19:10:04.201|
|{2024-08-27 19:09:50, 2024-08-27 19:10:00}|30   |2024-08-27 19:10:04.201|
|{2024-08-27 19:10:00, 2024-08-27 19:10:10}|12   |2024-08-27 19:10:04.201|
+------------------------------------------+-----+-----------------------+

```

#### 滑动窗口
滑动窗口(Sliding Window)与翻滚窗口类似，同样是一些列具有固定时间宽度的数据窗口，但当滑动时间小于窗口时间时，相邻的窗口间可能会有重叠，即同一条数据可能会出现在两个甚至多个滑动窗口中  
翻滚窗口其实是一种特殊的滑动窗口，翻滚一次移动的长度恰好等于窗口的宽度，即滑动的长度恰好等于窗口的宽度  
```scala
val startTime = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").format(LocalDateTime.now)
println(f"Job start at ${startTime}")

// create rate streaming DataFrame
val rateStreamingDataFrame: DataFrame = spark.readStream
  .format("rate")
  .option("rowsPerSecond", "3")
  .load()

rateStreamingDataFrame
  .groupBy(window(col("timestamp"), windowDuration = "10 seconds", slideDuration = "5 seconds")).count()
  .withColumn("current_time", current_timestamp())
  .orderBy(col("window"))
  .writeStream
  .outputMode("complete")
  .format("console").option("truncate", "false")
  .trigger(Trigger.ProcessingTime("5 seconds"))
  .start()
  .awaitTermination()
```
程序启动后，控制台将打印出每个批次每个窗口中的数据
``` 
Job start at 2024-08-27 19:29:19

-------------------------------------------
Batch: 0
-------------------------------------------
+------+-----+------------+
|window|count|current_time|
+------+-----+------------+
+------+-----+------------+

-------------------------------------------
Batch: 1
-------------------------------------------
+------------------------------------------+-----+-----------------------+
|window                                    |count|current_time           |
+------------------------------------------+-----+-----------------------+
|{2024-08-27 19:29:15, 2024-08-27 19:29:25}|6    |2024-08-27 19:29:50.899|
|{2024-08-27 19:29:20, 2024-08-27 19:29:30}|21   |2024-08-27 19:29:50.899|
|{2024-08-27 19:29:25, 2024-08-27 19:29:35}|30   |2024-08-27 19:29:50.899|
|{2024-08-27 19:29:30, 2024-08-27 19:29:40}|30   |2024-08-27 19:29:50.899|
|{2024-08-27 19:29:35, 2024-08-27 19:29:45}|30   |2024-08-27 19:29:50.899|
|{2024-08-27 19:29:40, 2024-08-27 19:29:50}|30   |2024-08-27 19:29:50.899|
|{2024-08-27 19:29:45, 2024-08-27 19:29:55}|15   |2024-08-27 19:29:50.899|
+------------------------------------------+-----+-----------------------+

-------------------------------------------
Batch: 2
-------------------------------------------
+------------------------------------------+-----+-----------------------+
|window                                    |count|current_time           |
+------------------------------------------+-----+-----------------------+
|{2024-08-27 19:29:15, 2024-08-27 19:29:25}|6    |2024-08-27 19:30:13.015|
|{2024-08-27 19:29:20, 2024-08-27 19:29:30}|21   |2024-08-27 19:30:13.015|
|{2024-08-27 19:29:25, 2024-08-27 19:29:35}|30   |2024-08-27 19:30:13.015|
|{2024-08-27 19:29:30, 2024-08-27 19:29:40}|30   |2024-08-27 19:30:13.015|
|{2024-08-27 19:29:35, 2024-08-27 19:29:45}|30   |2024-08-27 19:30:13.015|
|{2024-08-27 19:29:40, 2024-08-27 19:29:50}|30   |2024-08-27 19:30:13.015|
|{2024-08-27 19:29:45, 2024-08-27 19:29:55}|30   |2024-08-27 19:30:13.015|
|{2024-08-27 19:29:50, 2024-08-27 19:30:00}|30   |2024-08-27 19:30:13.015|
|{2024-08-27 19:29:55, 2024-08-27 19:30:05}|30   |2024-08-27 19:30:13.015|
|{2024-08-27 19:30:00, 2024-08-27 19:30:10}|30   |2024-08-27 19:30:13.015|
|{2024-08-27 19:30:05, 2024-08-27 19:30:15}|21   |2024-08-27 19:30:13.015|
|{2024-08-27 19:30:10, 2024-08-27 19:30:20}|6    |2024-08-27 19:30:13.015|
+------------------------------------------+-----+-----------------------+
```
#### 会话窗口
会话窗口(Session Window)具有和其他两种窗口不同的行为，它是以一次完整的会话为单位的，接收到数据时即为会话开始，当收到数据后超过给定时间没有新的数据到来，即认为本次会话结束，因此其窗口长度是不固定的，当会话一直结束不了时，不会产生新的会话窗口      
会话窗口必须指定某一列进行统计，不能进行全局统计   
```scala
val startTime = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").format(LocalDateTime.now)
println(f"Job start at ${startTime}")

// create rate streaming DataFrame
val rateStreamingDataFrame: DataFrame = spark.readStream
  .format("rate")
  .option("rowsPerSecond", "3")
  .load()

rateStreamingDataFrame
  .withColumn("is_odd", col("value") % 2)
  .groupBy(session_window(col("timestamp"), gapDuration = "1 seconds"), col("is_odd")).count()
  .withColumn("current_time", current_timestamp())
  .orderBy(col("session_window"))
  .writeStream
  .outputMode("complete")
  .format("console").option("truncate", "false")
  .trigger(Trigger.ProcessingTime("5 seconds"))
  .start()
  .awaitTermination()
```
程序启动后，控制台将打印出每个批次每个窗口中的数据，
``` 
Job start at 2024-08-27 19:42:13

-------------------------------------------
Batch: 0
-------------------------------------------
+--------------+------+-----+------------+
|session_window|is_odd|count|current_time|
+--------------+------+-----+------------+
+--------------+------+-----+------------+

-------------------------------------------
Batch: 1
-------------------------------------------
+--------------------------------------------------+------+-----+-----------------------+
|session_window                                    |is_odd|count|current_time           |
+--------------------------------------------------+------+-----+-----------------------+
|{2024-08-27 19:42:17.983, 2024-08-27 19:42:42.316}|0     |36   |2024-08-27 19:42:42.366|
|{2024-08-27 19:42:18.316, 2024-08-27 19:42:42.65} |1     |36   |2024-08-27 19:42:42.366|
+--------------------------------------------------+------+-----+-----------------------+

-------------------------------------------
Batch: 2
-------------------------------------------
+--------------------------------------------------+------+-----+-----------------------+
|session_window                                    |is_odd|count|current_time           |
+--------------------------------------------------+------+-----+-----------------------+
|{2024-08-27 19:42:17.983, 2024-08-27 19:42:58.316}|0     |60   |2024-08-27 19:42:58.853|
|{2024-08-27 19:42:18.316, 2024-08-27 19:42:58.65} |1     |60   |2024-08-27 19:42:58.853|
+--------------------------------------------------+------+-----+-----------------------+
```

#### 水印



## Sink 算子 
### 输出模式
#### append
#### complete
#### update 

### 输出到控制台
将流式 DataFrame 按批次输出到控制台  
```scala
// create rate streaming DataFrame
val rateStreamingDataFrame: DataFrame = spark.readStream
  .format("rate")
  .option("rowsPerSecond", "3")
  .load()

println(f"isStreaming = ${rateStreamingDataFrame.isStreaming}")

// print in console
rateStreamingDataFrame.writeStream
  .format("console")
  .option("truncate", "false")
  .trigger(Trigger.ProcessingTime("5 seconds"))
  .start()
  .awaitTermination()
```
程序启动后，控制台将打印出每个批次中的数据
``` 
isStreaming = true

-------------------------------------------
Batch: 1
-------------------------------------------
+--------------------+-----+
|           timestamp|value|
+--------------------+-----+
|2024-08-26 10:10:...|    0|
|2024-08-26 10:10:...|   10|
|2024-08-26 10:10:...|   20|
+--------------------+-----+
``` 
### 写入外部文件系统
### 转换为 Java 集合
### 

## 控制算子


