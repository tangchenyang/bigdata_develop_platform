package org.exmaple.spark.sparkstreaming

import org.apache.spark._
import org.apache.spark.streaming._

object SocketTextStreamExample {
  def main(args: Array[String]): Unit = {
    // create spark streaming context
    val sparkConf = new SparkConf().setMaster("local[*]").setAppName(this.getClass.getName)
    val ssc = new StreamingContext(sparkConf, Seconds(1))

    // create socket text stream
    val lines = ssc.socketTextStream("localhost", 9999)

    // split lines into words
    val words = lines.flatMap(_.split(" "))

    // count words
    val wordCounts = words
      .map(word => (word, 1))
      .reduceByKey(_ + _)

    // print in console
    wordCounts.print()

    // start streaming job
    ssc.start()

    // await for termination
    ssc.awaitTermination()
  }


}
