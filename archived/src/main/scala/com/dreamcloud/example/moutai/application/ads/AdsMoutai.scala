package com.dreamcloud.example.moutai.application.ads

import com.dreamcloud.common.application.DwdApplication
import com.dreamcloud.common.spark.dataframe.DataFrameReader
import com.dreamcloud.common.table.Table
import com.dreamcloud.example.moutai.table.ads.AdsTables
import com.dreamcloud.example.moutai.table.dwd.DwdTables
import com.dreamcloud.example.moutai.table.ods.OdsTables

object AdsMoutai extends DwdApplication {

  override def process(args: Array[String]): Unit = {
    val odsDf = DataFrameReader(spark).fromHive.table(input.head.tableName)
    odsDf.show()
  }

  override val input: Set[Table] = Set(
    DwdTables.dwd_moutai,
    DwdTables.dwd_moutai_1
  )
  override val output: Set[Table] = Set(AdsTables.ads_moutai)
}