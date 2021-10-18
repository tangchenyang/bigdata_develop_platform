package org.example.moutai

import org.example.moutai.application.dw.fact.DwFactMoutai
import org.example.util.scheduler.ApplicationScheduler

object TestScheduler extends App {
  ApplicationScheduler.register(DwFactMoutai)
  ApplicationScheduler.appSet.foreach(ap => println(ap.appName))
  ApplicationScheduler.allInputTables.foreach(table => println(table.tableName))
  ApplicationScheduler.allOutputTables.foreach(table => println(table.tableName))
}