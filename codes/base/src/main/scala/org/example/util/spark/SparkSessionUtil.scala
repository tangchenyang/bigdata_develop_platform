package org.example.util.spark

import org.apache.spark.sql.SparkSession

/**
 * utils about Spark Session
 */
object SparkSessionUtil {

  def getSparkSession = SparkSession
    .builder
    .master("local[*]")
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
    .enableHiveSupport()
    .getOrCreate

}
