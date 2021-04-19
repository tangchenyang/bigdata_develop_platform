package org.example.moutai.dw.fact

import org.example.util.application.FactApplication
import org.example.util.spark.dataframe.DataFrameReader
import org.example.util.table.Table

object DwFactMoutai extends FactApplication {

  override val appName: String = "DwFactMoutai"

  override def process(args: Array[String]): Unit = {
    val odsDf = DataFrameReader(spark).fromHive.table("example.ods_moutai")
    odsDf.show()
  }

  override val input: Set[Table] = null
  override val output: Set[_ <: Table] = null
}