package org.example.util.spark

import org.apache.spark.sql.Row

class SparkSessionUtilTest extends org.scalatest.FunSuite {

  test("test SparkSession") {
    val spark = SparkSessionUtil.sparkSessionOnLocal
    val df = spark.createDataFrame(Seq(
      Student(1,"Tom")
    ))
    val expected = Seq(
      Row(1, "Tom")
    )

    assert(df.collect === expected)
  }
}

case class Student(id: Long, name: String)
