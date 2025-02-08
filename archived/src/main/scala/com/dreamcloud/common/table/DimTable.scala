package com.dreamcloud.common.table

import com.dreamcloud.common.table.TableType.TableType

case class DimTable(
                     override val tableName: String,
                     override val tableDDL: String
                   ) extends Table(tableName, tableDDL) {
  override val tableType: TableType = TableType.DIM_TABLE
}
