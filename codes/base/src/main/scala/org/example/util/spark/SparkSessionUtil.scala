package org.example.util.spark

import org.apache.spark.sql.SparkSession
import org.example.util.LaunchMode
import org.example.util.application.SparkApplication

/**
 * utils about Spark Session
 */
object SparkSessionUtil {

  def sparkSessionOnLocal: SparkSession = SparkSession
    .builder
    .master("local[*]")
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
    .enableHiveSupport()
    .getOrCreate

  def sparkSessionWithoutMaster: SparkSession = SparkSession
    .builder
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse")
    .enableHiveSupport()
    .getOrCreate

  def getSparkSession: SparkSession = {
    SparkApplication.launchMode match {
      case LaunchMode.LOCAL => sparkSessionOnLocal
      case LaunchMode.YARN_CLIENT => sparkSessionWithoutMaster
      case LaunchMode.YARN_CLUSTER => sparkSessionWithoutMaster
    }
  }

}
