package com.dreamcloud.example.moutai.table.dw.fact

import com.dreamcloud.common.table.FactTable

object FactTables {

  val dw_fact_moutai: FactTable = FactTable(
    tableName = "dw_fact_moutai",
    tableDDL = "create table dw_fact_moutai () "
  )
  val dw_fact_moutai_1: FactTable = FactTable(
    tableName = "dw_fact_moutai_1",
    tableDDL = "create table dw_fact_moutai_1 () "
  )
}
