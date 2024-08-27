package org.exmaple.spark.structuredstreaming

import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.{DataFrame, SparkSession}

object TableSourceExample {
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
      .option("truncate", "false")
      .trigger(Trigger.ProcessingTime("2 seconds"))
      .start()
      .awaitTermination()








//    // print in console
//    rateStreamingDataFrame.writeStream
//      .format("console")
//      .trigger(Trigger.ProcessingTime("5 seconds"))
//      .start()
//      .awaitTermination()

  }
}
