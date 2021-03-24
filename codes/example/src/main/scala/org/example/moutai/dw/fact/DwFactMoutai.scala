package org.example.moutai.dw.fact

import org.example.util.job.FactJob
import org.example.util.spark.dataframe.DataFrameReader

object DwFactMoutai extends FactJob {

  override def process(): Unit = {
    spark.sql("show databases").show

    spark.sql("use example")
    spark.sql("show tables").show
    try{
      spark.sql("select * from example.ods_moutai").show
    } catch {
      case exception: Exception => System.err.println(exception.getMessage)
    }

    spark.table("example.ods_moutai").show


    val odsDf = DataFrameReader(spark).fromHive.table("example.ods_moutai")
    odsDf.show()
  }

}
