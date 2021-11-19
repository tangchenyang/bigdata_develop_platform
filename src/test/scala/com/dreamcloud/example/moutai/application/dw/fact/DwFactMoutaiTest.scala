package com.dreamcloud.example.moutai.application.dw.fact

import com.dreamcloud.common.metadata.Metadata
import org.scalatest.FunSuite

class DwFactMoutaiTest extends FunSuite {

  test("test scheduler for moutai") {
    Metadata.register(DwFactMoutai)
    Metadata.appSet.foreach(ap => println(ap.appName))
    Metadata.allInputTables.foreach(table => println(table.tableName))
    Metadata.allOutputTables.foreach(table => println(table.tableName))
  }

}
