package com.dreamcloud.example.moutai.application.dw.fact

import com.dreamcloud.common.application.FactApplication
import com.dreamcloud.common.spark.dataframe.DataFrameReader
import com.dreamcloud.common.table.Table
import com.dreamcloud.example.moutai.table.dw.fact.dw_fact_moutai
import com.dreamcloud.example.moutai.table.ods.ods_moutai

object DwFactMoutai extends FactApplication {

  override def process(args: Array[String]): Unit = {
    val odsDf = DataFrameReader(spark).fromHive.table("example.ods_moutai")
    odsDf.show()
  }

  override val input: Set[Table] = Set(ods_moutai)
  override val output: Set[Table] = Set(dw_fact_moutai)
}