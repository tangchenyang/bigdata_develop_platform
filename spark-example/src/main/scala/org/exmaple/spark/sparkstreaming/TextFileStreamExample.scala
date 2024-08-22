package org.exmaple.spark.sparkstreaming

import org.apache.spark._
import org.apache.spark.streaming._

object TextFileStreamExample {
  def main(args: Array[String]): Unit = {
    // create spark streaming context
    val sparkConf = new SparkConf().setMaster("local[*]").setAppName(this.getClass.getName)
    val ssc = new StreamingContext(sparkConf, Seconds(5))

    // create socket text stream
    val lines = ssc.textFileStream("/tmp/spark/logs/")

    // print in console
    lines.print()

    // start streaming job
    ssc.start()

    // await for termination
    ssc.awaitTermination()
  }


}
