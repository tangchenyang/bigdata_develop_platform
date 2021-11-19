package com.dreamcloud.common.table

import com.dreamcloud.common.table.TableType.TableType

case class OdsTable(
                     override val tableName: String,
                     override val tableDDL: String
                   ) extends Table(tableName, tableDDL) {
  override val tableType: TableType = TableType.ODS_TABLE
}
