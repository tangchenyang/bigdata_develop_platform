package org.example.util.table
import org.example.util.table.TableType.TableType

abstract class OdsTable extends Table {

  override val tableType: TableType = TableType.ODS_TABLE
}
