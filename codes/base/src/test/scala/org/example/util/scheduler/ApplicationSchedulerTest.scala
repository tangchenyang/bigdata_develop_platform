package org.example.util.scheduler

import org.example.util.application.{DimApplication, FactApplication, OdsApplication, SparkApplication}
import org.example.util.table.{AdsTable, DimTable, FactTable, OdsTable, Table, TableType}
import org.example.util.table.TableType.TableType
import org.scalatest.FunSuite

class ApplicationSchedulerTest extends FunSuite {

  test("test register") {

    val odsTable = new OdsTable {
      override val tableName: String = "ods table"
      override val tableType: TableType = TableType.ODS_TABLE
    }

    val odsApplication = new OdsApplication {
      override val appName: String = "ods application"

      override def process(args: Array[String]): Unit = {}

      override val input: Set[Table] = Set(odsTable)
      override val output: Set[_ <: Table] = Set(odsTable)
    }

    val factTable = new FactTable {
      override val tableName: String = "fact table"
      override val tableType: TableType = TableType.FACT_TABLE
    }

    val factApplication = new FactApplication {
      override val appName: String = "fact application"

      override def process(args: Array[String]): Unit = {}

      override val input: Set[Table] = Set(factTable)
      override val output: Set[_ <: Table] = Set(factTable)
    }

    val dimTable = new DimTable {
      override val tableName: String = "dim table"
      override val tableType: TableType = TableType.DIM_TABLE
    }

    val dimApplication = new DimApplication {
      override val appName: String = "dim application"

      override def process(args: Array[String]): Unit = {}

      override val input: Set[Table] = Set(dimTable)
      override val output: Set[_ <: Table] = Set(dimTable)
    }


    ApplicationScheduler.register(odsApplication)
    ApplicationScheduler.register(factApplication)
    ApplicationScheduler.register(dimApplication)

    ApplicationScheduler.appSet.foreach(app => println(app.appName))
    ApplicationScheduler.printAllDependencies()
  }

}
