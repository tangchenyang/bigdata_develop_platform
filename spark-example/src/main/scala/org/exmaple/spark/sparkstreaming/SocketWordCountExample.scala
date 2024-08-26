package org.exmaple.spark.sparkstreaming

import org.apache.spark._
import org.apache.spark.streaming._

object SocketWordCountExample {
  def main(args: Array[String]): Unit = {
    // create spark streaming context
    val sparkConf = new SparkConf().setMaster("local[*]").setAppName(this.getClass.getName)
    val ssc = new StreamingContext(sparkConf, Seconds(5))

    // create socket text stream
    val socketTextDStream = ssc.socketTextStream("localhost", 9999)

    // split lines into words
    val wordsDStream = socketTextDStream
      .flatMap(_.split(" "))

    // count words
    val wordCountsDStream = wordsDStream
      .map((_, 1))
      .reduceByKey(_ + _)

    // print in console
    wordCountsDStream.print()

    // start streaming job
    ssc.start()

    // await for termination
    ssc.awaitTermination()
  }


}
