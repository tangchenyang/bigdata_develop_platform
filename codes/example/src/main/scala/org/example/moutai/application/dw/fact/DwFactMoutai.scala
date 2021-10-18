package org.example.moutai.application.dw.fact

import org.example.moutai.table.dw.fact.dw_fact_moutai
import org.example.moutai.table.ods.ods_moutai
import org.example.util.application.FactApplication
import org.example.util.spark.dataframe.DataFrameReader
import org.example.util.table.Table

object DwFactMoutai extends FactApplication {

  override def process(args: Array[String]): Unit = {
    val odsDf = DataFrameReader(spark).fromHive.table("example.ods_moutai")
    odsDf.show()
  }

  override val input: Set[Table] = Set(ods_moutai)
  override val output: Set[Table] = Set(dw_fact_moutai)
}