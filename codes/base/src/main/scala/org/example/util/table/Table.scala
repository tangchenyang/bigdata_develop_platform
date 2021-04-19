package org.example.util.table

import org.example.util.table.TableType.TableType

abstract class Table {
  val tableName: String
  val tableType: TableType
}
