package com.dreamcloud.example.moutai.application.dwd

import com.dreamcloud.common.application.DwdApplication
import com.dreamcloud.common.spark.dataframe.DataFrameReader
import com.dreamcloud.common.table.Table
import com.dreamcloud.example.moutai.table.dwd.DwdTables
import com.dreamcloud.example.moutai.table.ods.OdsTables

object DwdMoutai1 extends DwdApplication {

  override def process(args: Array[String]): Unit = {
    val odsDf = DataFrameReader(spark).fromHive.table(input.head.tableName)
    odsDf.show()
  }

  override val input: Set[Table] = Set(
    OdsTables.ods_moutai,
    OdsTables.ods_moutai_3,
    OdsTables.ods_moutai_4
  )
  override val output: Set[Table] = Set(DwdTables.dwd_moutai_1)
}
