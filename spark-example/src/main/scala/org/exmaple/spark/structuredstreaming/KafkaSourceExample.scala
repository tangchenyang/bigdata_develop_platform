package org.exmaple.spark.structuredstreaming

import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.{DataFrame, SparkSession}

object KafkaSourceExample {
  def main(args: Array[String]): Unit = {
    // create spark session
    val spark = SparkSession.builder.appName("Structured Streaming Example")
      .master("local[*]")
      .getOrCreate()

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

  }
}
