package com.dreamcloud.common.table

object TableType extends Enumeration {
  type TableType = Value
  val ODS_TABLE: TableType = Value
  val DWD_TABLE: TableType = Value
  val DIM_TABLE: TableType = Value
  val DWS_TABLE: TableType = Value
  val ADS_TABLE: TableType = Value
}
