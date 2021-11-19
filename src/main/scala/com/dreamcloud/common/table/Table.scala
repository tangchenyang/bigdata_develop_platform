package com.dreamcloud.common.table

import com.dreamcloud.common.table.TableType.TableType

abstract class Table(
                      val tableName: String,
                      val tableDDL: String
                    ) {

  var tableType: TableType

}
