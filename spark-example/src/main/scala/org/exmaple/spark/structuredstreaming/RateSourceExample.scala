package org.exmaple.spark.structuredstreaming

import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.{DataFrame, SparkSession}

object RateSourceExample {
  def main(args: Array[String]): Unit = {
    // create spark session
    val spark = SparkSession.builder.appName("Structured Streaming Example")
      .master("local[*]")
      .getOrCreate()

    // create rate streaming DataFrame
    val rateStreamingDataFrame: DataFrame = spark.readStream
      .format("rate")
      .option("rowsPerSecond", "3")
      .load()

    println(f"isStreaming = ${rateStreamingDataFrame.isStreaming}")

    // print in console
    rateStreamingDataFrame.writeStream
      .format("console")
      .trigger(Trigger.ProcessingTime("5 seconds"))
      .start()
      .awaitTermination()

  }
}
