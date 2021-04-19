package org.example.util.table

object TableType extends Enumeration {
  type TableType = Value
  val ODS_TABLE: TableType = Value
  val FACT_TABLE: TableType = Value
  val DIM_TABLE: TableType = Value
  val DM_TABLE: TableType = Value
  val ADS_TABLE: TableType = Value
}
