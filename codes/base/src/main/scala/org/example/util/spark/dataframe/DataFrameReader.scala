package org.example.util.spark.dataframe

import org.apache.spark.sql.{DataFrame, SparkSession}

case class DataFrameReader(spark: SparkSession) {

  object fromHive {
    def table(tableName: String): DataFrame = {
      spark.table(tableName)
    }

    def sql(sql: String) = {
      spark.sql(sql)
    }

  }
}
