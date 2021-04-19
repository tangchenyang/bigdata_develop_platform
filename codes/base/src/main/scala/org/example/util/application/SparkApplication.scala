package org.example.util.application

import org.apache.spark.sql.SparkSession
import org.example.util.LaunchMode
import org.example.util.LaunchMode.LaunchMode
import org.example.util.spark.SparkSessionUtil
import org.example.util.table.Table

abstract class SparkApplication {

  lazy val spark: SparkSession = SparkSessionUtil.getSparkSession

  val appName: String

  def process(args: Array[String]): Unit

  def main(args: Array[String]): Unit = {
    process(args)
    spark.close()
  }

  val input: Set[Table]

  val output: Set[Table] // 不同的App实现能否指定不同的Table实现
}

object SparkApplication {
  var launchMode: LaunchMode = defaultLaunchMode
  def defaultLaunchMode: LaunchMode = LaunchMode.YARN_CLIENT
}