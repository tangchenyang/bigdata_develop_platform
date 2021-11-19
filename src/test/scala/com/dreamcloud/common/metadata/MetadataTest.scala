package com.dreamcloud.common.metadata

import com.dreamcloud.common.application.{DimApplication, FactApplication, OdsApplication}
import com.dreamcloud.common.table.{DimTable, FactTable, OdsTable, Table}
import org.scalatest.FunSuite

class MetadataTest extends FunSuite {

  test("test register") {

    val odsTable = OdsTable(
      tableName = "ods table",
      tableDDL = ""
    )

    val odsApplication = new OdsApplication {
      override val appName: String = "ods application"

      override def process(args: Array[String]): Unit = {}

      override val output: Set[Table] = Set(odsTable)
    }


    val dimTable = DimTable (
        tableName = "dim table",
        tableDDL = ""
    )

    val dimApplication = new DimApplication {
      override val appName: String = "dim application"

      override def process(args: Array[String]): Unit = {}

      override val input: Set[Table] = Set(odsTable)
      override val output: Set[Table] = Set(dimTable)
    }

    val factTable = FactTable(
      tableName = "fact table",
      tableDDL = ""
    )

    val factApplication = new FactApplication {
      override val appName: String = "fact application"

      override def process(args: Array[String]): Unit = {}

      override val input: Set[Table] = Set(odsTable, dimTable)
      override val output: Set[Table] = Set(factTable)
    }


    Metadata.register(odsApplication)
    Metadata.register(factApplication)
    Metadata.register(dimApplication)

    assert(Metadata.appSet.map(_.appName) === Set("ods application", "dim application", "fact application"))
    assert(Metadata.allInputTables.map(_.tableName) === Set("ods table", "dim table"))
    assert(Metadata.allOutputTables.map(_.tableName) === Set("ods table", "dim table", "fact table"))

  }

}
