package org.example.util.spark

import org.example.util.spark.SparkSessionUtil.getSparkSession

class SparkSessionUtilTest extends org.scalatest.FunSuite {

  test("test SparkSession") {
    val spark = getSparkSession
    val df = spark.createDataFrame(Seq(
      Student(1,"Tom")
    ))
    val expected = Seq((1, "Tom"))

    assert(df.collect === expected)
  }
}

case class Student(id: Long, name: String)