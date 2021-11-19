package com.dreamcloud.common.table

import com.dreamcloud.common.table.TableType.TableType

case class AdsTable(
                     override val tableName: String,
                     override val tableDDL: String
                   ) extends Table(tableName, tableDDL) {
  override var tableType: TableType = TableType.ADS_TABLE
}
