package com.dreamcloud.example.moutai.application.ads

import com.dreamcloud.common.application.FactApplication
import com.dreamcloud.common.spark.dataframe.DataFrameReader
import com.dreamcloud.common.table.Table
import com.dreamcloud.example.moutai.table.ads.AdsTables
import com.dreamcloud.example.moutai.table.dw.fact.FactTables
import com.dreamcloud.example.moutai.table.ods.OdsTables

object AdsMoutai extends FactApplication {

  override def process(args: Array[String]): Unit = {
    val odsDf = DataFrameReader(spark).fromHive.table(input.head.tableName)
    odsDf.show()
  }

  override val input: Set[Table] = Set(
    FactTables.dw_fact_moutai,
    FactTables.dw_fact_moutai_1
  )
  override val output: Set[Table] = Set(AdsTables.ads_moutai)
}