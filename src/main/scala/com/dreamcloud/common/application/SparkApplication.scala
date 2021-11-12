package com.dreamcloud.common.application

import com.dreamcloud.common.LaunchMode
import com.dreamcloud.common.LaunchMode.LaunchMode
import com.dreamcloud.common.spark.SparkSessionUtil
import com.dreamcloud.common.table.Table
import org.apache.spark.sql.SparkSession

abstract class SparkApplication {

  lazy val spark: SparkSession = SparkSessionUtil.getSparkSession

  val appName: String = this.getClass.getSimpleName.replaceAll("\\$", "")

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