package com.dreamcloud.example.moutai.application.dwd

import com.dreamcloud.common.application.DwdApplication
import com.dreamcloud.common.spark.dataframe.DataFrameReader
import com.dreamcloud.common.table.Table
import com.dreamcloud.example.moutai.table.dwd.DwdTables
import com.dreamcloud.example.moutai.table.ods.OdsTables

object DwdMoutai extends DwdApplication {

  override def process(args: Array[String]): Unit = {
    val odsDf = DataFrameReader(spark).fromHive.table(input.head.tableName)
    odsDf.show()
  }

  override val input: Set[Table] = Set(
    OdsTables.ods_moutai,
    OdsTables.ods_moutai_1,
    OdsTables.ods_moutai_2
  )
  override val output: Set[Table] = Set(DwdTables.dwd_moutai)
}
