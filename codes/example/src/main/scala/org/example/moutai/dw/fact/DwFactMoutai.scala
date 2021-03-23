package org.example.moutai.dw.fact

import org.example.util.job.FactJob
import org.example.util.spark.dataframe.DataFrameReader

object DwFactMoutai extends FactJob {

  override def process(): Unit = {
    val odsDf = DataFrameReader(spark).fromHive.table("example.ods_moutai")
    odsDf.show()
  }

}
