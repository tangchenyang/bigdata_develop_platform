package com.dreamcloud.common.table

import com.dreamcloud.common.table.TableType.TableType

abstract class OdsTable extends Table {

  override val tableType: TableType = TableType.ODS_TABLE
}
