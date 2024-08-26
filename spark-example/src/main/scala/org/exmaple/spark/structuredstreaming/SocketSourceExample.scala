package org.exmaple.spark.structuredstreaming

import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.{DataFrame, SparkSession}

object SocketSourceExample {
  def main(args: Array[String]): Unit = {
    // create spark session
    val spark = SparkSession.builder.appName("Structured Streaming Example")
      .master("local[*]")
      .getOrCreate()

    // create socket streaming DataFrame
    val socketStreamingDataFrame: DataFrame = spark.readStream
      .format("socket")
      .option("host", "localhost")
      .option("port", 9999)
      .load()

    println(f"isStreaming = ${socketStreamingDataFrame.isStreaming}")

    // print in console
    socketStreamingDataFrame.writeStream
      .format("console")
      .trigger(Trigger.ProcessingTime("5 seconds"))
      .start()
      .awaitTermination()

  }
}
