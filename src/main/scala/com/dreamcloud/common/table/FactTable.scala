package com.dreamcloud.common.table

import com.dreamcloud.common.table.TableType.TableType

abstract class FactTable extends Table {

  override val tableType: TableType = TableType.FACT_TABLE
}
