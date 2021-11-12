package com.dreamcloud.example.moutai.table.dw.fact

import com.dreamcloud.common.table.FactTable

object dw_fact_moutai extends FactTable {
  override val tableName: String = "dw_fact_moutai"
  override val tableDDL: String = "create table dw_fact_moutai ( )"
}
