package org.example.util.table
import org.example.util.table.TableType.TableType

abstract class FactTable extends Table {

  override val tableType: TableType = TableType.FACT_TABLE
}
