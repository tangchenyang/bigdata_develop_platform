package org.example.util.job

import org.apache.spark.sql.SparkSession
import org.example.util.spark.SparkSessionUtil

class SparkJob {
  lazy val spark: SparkSession = SparkSessionUtil.getSparkSession

  def process() = {}

  def main(args: Array[String]): Unit = {

    process()

    spark.close()
  }

}
