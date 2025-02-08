package com.dreamcloud.example.moutai.table.dwd

import com.dreamcloud.common.table.DwdTable

object DwdTables {

  val dwd_moutai: DwdTable = DwdTable(
    tableName = "dwd_moutai",
    tableDDL = "create table dwd_moutai () "
  )
  val dwd_moutai_1: DwdTable = DwdTable(
    tableName = "dwd_moutai_1",
    tableDDL = "create table dwd_moutai_1 () "
  )
}
