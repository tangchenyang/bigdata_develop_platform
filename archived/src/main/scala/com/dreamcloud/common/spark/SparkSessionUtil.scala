package com.dreamcloud.common.spark

import com.dreamcloud.common.LaunchMode
import com.dreamcloud.common.application.SparkApplication
import org.apache.spark.sql.SparkSession

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
