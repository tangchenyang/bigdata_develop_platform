package org.exmaple.spark.structuredstreaming

import org.apache.spark.sql._
import org.apache.spark.sql.streaming.Trigger

object FileSystemSourceExample {
  def main(args: Array[String]): Unit = {
    // create spark session
    val spark = SparkSession.builder.appName("Structured Streaming Example")
      .master("local[*]")
      .getOrCreate()

    // create text file streaming DataFrame
    val textFilesStreamingDataFrame: DataFrame = spark.readStream
      .option("header", "false")
      .text("file:///tmp/spark/input_txt_files/")

    println(f"isStreaming = ${textFilesStreamingDataFrame.isStreaming}")

    // print in console
    textFilesStreamingDataFrame.writeStream
      .format("console")
      .trigger(Trigger.ProcessingTime("5 seconds"))
      .start()
      .awaitTermination()

  }
}
