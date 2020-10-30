package com.chenyangtang.util

import org.apache.spark.sql.{DataFrame, SaveMode}

object MyImplicits {
  implicit def turnToMyDFWriter(df: DataFrame) = new MyDataFrameWriter(df)
}

class MyDataFrameWriter(df: DataFrame) {

  def insertIntoHive(dbName: String,
                     tableName: String,
                     saveMode: SaveMode = SaveMode.Overwrite): Unit = {
    df.write.mode(saveMode).saveAsTable(s"$dbName.$tableName")

  }

}
