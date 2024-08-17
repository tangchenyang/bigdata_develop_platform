package org.exmaple.spark.sparkstreaming

import org.apache.spark._
import org.apache.spark.storage.StorageLevel
import org.apache.spark.streaming._
import org.apache.spark.streaming.dstream.ReceiverInputDStream

import java.io._
import scala.collection.JavaConverters._

object SocketStreamExample {
  def main(args: Array[String]): Unit = {
    // create spark streaming context
    val sparkConf = new SparkConf().setMaster("local[*]").setAppName(this.getClass.getName)
    val ssc = new StreamingContext(sparkConf, Seconds(1))

    // define class WordCount
    case class WordCount(word: String, count: Int) extends Serializable

    // define custom converter
    def convertBytesToWords(inputStream: InputStream): Iterator[WordCount] = {
      val dataInputStream = new BufferedReader(
        new InputStreamReader(inputStream, "UTF-8")
      )
      val linesIterator = dataInputStream.lines().iterator().asScala
      val wordsIterator = linesIterator.flatMap(_.split(" "))
      val wordCountIterator = wordsIterator.map(new WordCount(_, 1))
      wordCountIterator
    }

    // create socket stream
    val socketWordCountDStream: ReceiverInputDStream[WordCount] = ssc.socketStream[WordCount](
      "localhost", 9999, convertBytesToWords, StorageLevel.MEMORY_AND_DISK_SER_2
    )
    // count words
    val wordCounts = socketWordCountDStream
      .map(wc => (wc.word, wc.count))
      .reduceByKey(_ + _)
      .map { case (word, count) => new WordCount(word, count) }

    // print in console
    wordCounts.print()

    // start streaming job
    ssc.start()

    // await for termination
    ssc.awaitTermination()
  }

}
