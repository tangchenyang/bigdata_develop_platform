package com.dreamcloud.example.moutai.application.dw.fact

import com.dreamcloud.common.application.FactApplication
import com.dreamcloud.common.spark.dataframe.DataFrameReader
import com.dreamcloud.common.table.Table
import com.dreamcloud.example.moutai.table.dw.fact.FactTables
import com.dreamcloud.example.moutai.table.ods.OdsTables

object DwFactMoutai1 extends FactApplication {

  override def process(args: Array[String]): Unit = {
    val odsDf = DataFrameReader(spark).fromHive.table(input.head.tableName)
    odsDf.show()
  }

  override val input: Set[Table] = Set(
    OdsTables.ods_moutai,
    OdsTables.ods_moutai_3,
    OdsTables.ods_moutai_4
  )
  override val output: Set[Table] = Set(FactTables.dw_fact_moutai_1)
}