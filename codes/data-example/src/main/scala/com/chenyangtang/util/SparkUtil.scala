package com.chenyangtang.util

import org.apache.spark.sql.SparkSession

object SparkUtil {

  def getSparkSession(appName: String): SparkSession =
    SparkSession.builder.appName(appName).getOrCreate

}
