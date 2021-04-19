package org.example.util.application

import org.apache.spark.sql.SparkSession
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

  val input:Set[Table]

  val output: Set[ _ <: Table]


}
