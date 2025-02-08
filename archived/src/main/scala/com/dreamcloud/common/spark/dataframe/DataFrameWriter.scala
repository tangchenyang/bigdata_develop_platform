package com.dreamcloud.common.spark.dataframe

import org.apache.spark.sql.{DataFrame, SaveMode}

case class DataFrameWriter(dataframe: DataFrame) {

  object toHive {
    def table(tableName: String) = {
      dataframe.write.mode(SaveMode.Overwrite).saveAsTable(tableName)
    }
  }
}
