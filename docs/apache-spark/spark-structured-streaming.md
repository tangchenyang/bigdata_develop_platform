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
Structured Streaming 提供了一个 `Rate Source` 用于按照 `rowsPerSecond` 的速率生成测试场景下的输入数据   
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
|2024-10-10 10:10:...|    0|
|2024-10-10 10:10:...|   10|
|2024-10-10 10:10:...|   20|
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

## Transformation 算子
### 基本转换
### 聚合操作
### 分区转换
### 集合运算
### 窗口函数
### 水印
### 

## Action 算子 
### 写入外部文件系统
### 

## 控制算子


