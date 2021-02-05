package org.example.util.spark

import org.apache.spark.sql.SparkSession

/**
 * utils about Spark Session
 */
object SparkSessionUtil {

  def getSparkSession = SparkSession
    .builder
    .master("local[*]")
    .getOrCreate

}
