package com.chenyangtang.etl

import com.chenyangtang.util.SparkUtil

/**
 * todo wating for testing
 */
object EtlExample {
  def main(args: Array[String]): Unit = {
    val spark = SparkUtil.getSparkSession(this.getClass.getName)
    val personDF = spark.sql("select * from ods.test_person")
    import com.chenyangtang.util.MyImplicits._
    personDF.insertIntoHive("ods","test_person")
  }

}
